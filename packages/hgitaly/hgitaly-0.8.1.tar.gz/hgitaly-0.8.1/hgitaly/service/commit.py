# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import logging

from hgext3rd.heptapod.branch import get_default_gitlab_branch
from google.protobuf.timestamp_pb2 import Timestamp
from mercurial import (
    util,
    error,
    pycompat,
    logcmdutil,
    hgweb,
)

from ..errors import (
    internal_error,
    not_implemented,
)
from ..stub.commit_pb2 import (
    CommitIsAncestorRequest,
    CommitIsAncestorResponse,
    TreeEntryRequest,
    TreeEntryResponse,
    CommitsBetweenRequest,
    CommitsBetweenResponse,
    CountCommitsRequest,
    CountCommitsResponse,
    CountDivergingCommitsRequest,
    CountDivergingCommitsResponse,
    GetTreeEntriesRequest,
    GetTreeEntriesResponse,
    ListFilesRequest,
    ListFilesResponse,
    FindCommitRequest,
    FindCommitResponse,
    CommitStatsRequest,
    CommitStatsResponse,
    FindAllCommitsRequest,
    FindAllCommitsResponse,
    FindCommitsRequest,
    FindCommitsResponse,
    CommitLanguagesRequest,
    CommitLanguagesResponse,
    RawBlameRequest,
    RawBlameResponse,
    LastCommitForPathRequest,
    LastCommitForPathResponse,
    ListLastCommitsForTreeRequest,
    ListLastCommitsForTreeResponse,
    CommitsByMessageRequest,
    CommitsByMessageResponse,
    ListCommitsByOidRequest,
    ListCommitsByOidResponse,
    ListCommitsByRefNameRequest,
    ListCommitsByRefNameResponse,
    FilterShasWithSignaturesRequest,
    FilterShasWithSignaturesResponse,
    GetCommitSignaturesRequest,
    GetCommitSignaturesResponse,
    GetCommitMessagesRequest,
    GetCommitMessagesResponse,
)
from ..stub.commit_pb2_grpc import CommitServiceServicer

from .. import message
from ..revision import gitlab_revision_changeset
from ..servicer import HGitalyServicer
from ..util import chunked

logger = logging.getLogger(__name__)


class CommitServicer(CommitServiceServicer, HGitalyServicer):

    def CommitIsAncestor(self,
                         request: CommitIsAncestorRequest,
                         context) -> CommitIsAncestorResponse:
        # The question is legit for filtered changesets and that
        # happens in MR rebase scenarios, before the Rails app realizes
        # the MR has to be updated.
        repo = self.load_repo(request.repository, context).unfiltered()
        # TODO status.Errorf(codes.InvalidArgument, "Bad Request
        # (empty ancestor sha)") and same for child
        try:
            ancestor = repo[request.ancestor_id.encode()]
            child = repo[request.child_id.encode()]
        except error.RepoLookupError as exc:
            # Gitaly just returns False. This is probably an inconsistency
            # in the client, so let's log it to help.
            logger.warning(
                "CommitIsAncestor for child_id=%r, ancestor_id=%r, got %r",
                request.ancestor_id, request.child_id, exc)
            result = False
        else:
            result = ancestor.isancestorof(child)

        return CommitIsAncestorResponse(value=result)

    def TreeEntry(self, request: TreeEntryRequest,
                  context) -> TreeEntryResponse:
        return not_implemented(context, TreeEntryResponse,
                               issue=16)  # pragma no cover

    def CommitsBetween(self,
                       request: CommitsBetweenRequest,
                       context) -> CommitsBetweenResponse:
        """Stream chunks of commits "between" two GitLab revisions.

        One may believe the meaning of "between" to be based on DAG ranges,
        but actually, what the Gitaly reference Golang implementation does is
        ``git log --reverse FROM..TO``, which is indeed commonly used to obtain
        exclusive DAG ranges (would be `FROM::TO - FROM`) but gitrevisions(1)
        actually says:
           you can ask for commits that are reachable
           from r2 excluding those that are reachable from r1 by ^r1 r2
           and it can be written as r1..r2.

        So the true Mercurial equivalent revset is actually `TO % FROM`,
        which is quite different if FROM is not an ancestor of TO.

        Sadly, we happen to know `%` to be less efficient than DAG ranges.

        TODO: assuming the most common use case is indeed to obtain DAG ranges,
        (for which GitLab would actually have to check ancestry first), maybe
        introduce a direct call for DAG ranges later.
        TODO: find out if there are default values to apply for ``from`` and
              ``to``
        """
        repo = self.load_repo(request.repository, context)
        unfi = repo.unfiltered()
        rev_from = gitlab_revision_changeset(repo, getattr(request, 'from'))
        rev_to = gitlab_revision_changeset(repo, getattr(request, 'to'))

        # logging potentially both resolution failures
        if rev_from is None:
            logger.warning("cannot resolve 'from' revision in %r", request)
        if rev_to is None:
            logger.warning("cannot resolve 'to' revision in %r", request)

        if rev_from is None or rev_to is None:
            revs = []
        else:
            revs = unfi.revs('only(%s, %s)', rev_to, rev_from)

        for chunk in chunked(revs):
            yield CommitsBetweenResponse(
                commits=(message.commit(unfi[rev]) for rev in chunk))

    def CountCommits(self,
                     request: CountCommitsRequest,
                     context) -> CountCommitsResponse:
        # TODO: yet to finish this method to support all lookups
        repo = self.load_repo(request.repository, context)
        revision = request.revision
        # revision can be a pseudo range, like b'12340f9b5..a5f36b6a53012',
        # (see CommitsBetween for how we handle that)
        # (used in MR widget)
        if revision:
            if b'..' in revision:
                # TODO also case of ... (3 dots), I suppose
                ctx_start, ctx_end = [gitlab_revision_changeset(repo, rev)
                                      for rev in revision.split(b'..')]
                if ctx_start is None or ctx_end is None:
                    logger.warning(
                        "CountCommits for %r: one of these revisions "
                        "could not be found", revision)
                    return CountCommitsResponse()

                revs = repo.revs('only(%s, %s)', ctx_end, ctx_start)
            else:
                ctx = gitlab_revision_changeset(repo, revision)
                if ctx is None:
                    logger.warning(
                        "CountCommits revision %r could not be found",
                        revision)
                    return CountCommitsResponse()
                revs = repo.revs('::%s', ctx)
            count = len(revs)
        else:
            # Note: if revision is not passed, we return all revs for now.
            # `revision` and `all` are mutually exclusive
            count = len(repo)
        max_count = request.max_count
        if max_count and count > max_count:
            count = max_count
        return CountCommitsResponse(count=count)

    # CountDivergingCommits counts the diverging commits between from and to.
    # Important to note that when --max-count is applied, the counts are not
    # guaranteed to be accurate.

    def CountDivergingCommits(self,
                              request: CountDivergingCommitsRequest,
                              context) -> CountDivergingCommitsResponse:
        repo = self.load_repo(request.repository, context)
        rev_from = gitlab_revision_changeset(repo, getattr(request, 'from'))
        rev_to = gitlab_revision_changeset(repo, getattr(request, 'to'))
        max_count = request.max_count
        if rev_from is None:
            logger.warning("cannot resolve 'from' revision in %r", request)
        if rev_to is None:
            logger.warning("cannot resolve 'to' revision in %r", request)
        if rev_from is None or rev_to is None:
            return CountDivergingCommitsResponse(left_count=0, right_count=0)
        left = rev_from.rev()
        right = rev_to.rev()
        branchpoint = repo.revs(b"ancestor(%d, %d)" % (left, right)).first()
        left_count = len(repo.revs(b"%d::%d - %d" %
                                   (branchpoint, left, branchpoint)))
        right_count = len(repo.revs(b"%d::%d - %d" %
                                    (branchpoint, right, branchpoint)))
        if max_count and (left_count + right_count) > max_count:
            delta = (left_count + right_count) - max_count
            if left_count >= delta:
                left_count -= delta
            else:
                delta -= left_count
                left_count = 0
                right_count -= delta
        return CountDivergingCommitsResponse(left_count=left_count,
                                             right_count=right_count)

    def GetTreeEntries(self, request: GetTreeEntriesRequest,
                       context) -> GetTreeEntriesResponse:
        return not_implemented(context, GetTreeEntriesResponse,
                               issue=16)  # pragma no cover

    def ListFiles(self, request: ListFilesRequest,
                  context) -> ListFilesResponse:
        return not_implemented(context, ListFilesResponse,
                               issue=13)  # pragma no cover

    def CommitStats(self, request: CommitStatsRequest,
                    context) -> CommitStatsResponse:
        repo = self.load_repo(request.repository, context)
        revision = pycompat.sysbytes(request.revision)
        logger.debug("CommitStats revision=%r", revision)
        ctx = gitlab_revision_changeset(repo, revision)
        if ctx is None:
            return internal_error(
                context, CommitStatsResponse,
                "failed to get commit stats: object not found.",
                log_level=logging.WARNING
            )
        ctxp1 = ctx.p1()
        statsgen = hgweb.webutil.diffstatgen(repo.ui, ctx, ctxp1)
        # stats format:
        #   (list_of_stats_per_file, maxname,
        #    maxtotal, addtotal, removetotal, binary)
        # we only need addtotal and removetotal for our use case
        stats = next(statsgen)
        addtotal, removetotal = stats[-3], stats[-2]
        return CommitStatsResponse(
            oid=ctx.hex(),
            additions=addtotal,
            deletions=removetotal,
        )

    def FindCommit(self,
                   request: FindCommitRequest, context) -> FindCommitResponse:
        repo = self.load_repo(request.repository, context)
        revision = request.revision
        logger.debug("FindCommit revision=%r", revision)
        ctx = gitlab_revision_changeset(repo, revision)

        if ctx is None:
            logger.warning(
                "FindCommit revision %r could not be found",
                revision)
            return FindCommitResponse()

        commit = message.commit(ctx)
        return FindCommitResponse(commit=commit)

    def FindAllCommits(self, request: FindAllCommitsRequest,
                       context) -> FindAllCommitsResponse:
        repo = self.load_repo(request.repository, context)
        revision = request.revision
        opts = {}
        if revision:
            # If false, return all commits reachable by any branch in the repo
            logger.debug("FindAllCommits revision=%r", revision)
            ctx = gitlab_revision_changeset(repo, revision)
            if ctx is None:
                logger.debug(
                    "FindAllCommits revision %r could not be found",
                    revision)
                return FindAllCommitsResponse()
            revset = b"reverse(::%s)" % ctx
            opts[b'rev'] = [revset]
            # if ctx is an obsolete changeset, its repo is unfiltered.
            # this is legitimate if revision is a direct hash and should
            # not happen otherwise
            repo = ctx.repo()
        # gracinet: when we remove that compat, we can simply
        # just use repos.revs(), since logcmdutil does not seem to be
        # useful for this case (no `pats`) and is obviously a compatibility
        # hazard in itself.
        if util.versiontuple(n=2) <= (5, 5):
            revs, _ = logcmdutil.getrevs(repo, pats=(), opts=opts)  # hg<=5.5
        else:  # hg>5.5
            walk_opts = logcmdutil.parseopts(repo.ui, pats=(), opts=opts)
            revs, _ = logcmdutil.getrevs(repo, walk_opts)
        offset = request.skip
        if offset and offset > 0:
            revs = revs.slice(offset, len(revs))
        if request.max_count:
            revs = revs.slice(0, request.max_count)
        if request.order == FindAllCommitsRequest.TOPO:
            revs = repo.revs(b"sort(%ld, topo)", revs)
        elif request.order == FindAllCommitsRequest.DATE:
            revs = repo.revs(b"reverse(sort(%ld, date))", revs)
        for chunk in chunked(revs):
            yield FindAllCommitsResponse(
                commits=(message.commit(repo[rev]) for rev in chunk))

    def FindCommits(self, request: FindCommitsRequest,
                    context) -> FindCommitsResponse:
        repo = self.load_repo(request.repository, context)
        pats = request.paths
        # XXX: raise error if one of the path given is an empty string
        if pats:
            pats = list(map(lambda p: repo.root + b'/' + p, pats))
        opts = parse_find_commits_request_opts(request, repo)
        if request.revision and not opts[b'rev'][0]:
            logger.debug(
                "FindCommits revision %r could not be found",
                request.revision)
            return FindCommitsResponse()
        if util.versiontuple(n=2) <= (5, 5):  # hg<=5.5
            if request.follow and opts.get(b'rev'):
                # Mercurial 5.5: 'follow' option of `hg log` doesn't work
                # well when --rev option is set. For e.g. try
                # `hg log <file> --follow -r 'all()'`
                del opts[b'rev']
            revs, _ = logcmdutil.getrevs(repo, pats, opts)
        else:  # hg>5.5
            walk_opts = logcmdutil.parseopts(repo.ui, pats, opts)
            revs, _ = logcmdutil.getrevs(repo, walk_opts)
        offset = request.offset
        if offset > 0:
            revs = revs.slice(offset, len(revs))
        if request.order == FindCommitsRequest.TOPO:
            revs = repo.revs(b"sort(%ld, topo)", revs)
            if request.all:
                revs = repo.revs(b"reverse(%ld)", revs)
        for chunk in chunked(revs):
            yield FindCommitsResponse(
                commits=(message.commit(repo[rev]) for rev in chunk))

    def CommitLanguages(self, request: CommitLanguagesRequest,
                        context) -> CommitLanguagesResponse:
        return not_implemented(context, CommitLanguagesResponse,
                               issue=12)  # pragma no cover

    def RawBlame(self, request: RawBlameRequest,
                 context) -> RawBlameResponse:
        return not_implemented(context, RawBlameResponse,
                               issue=20)   # pragma no cover

    def LastCommitForPath(self,
                          request: LastCommitForPathRequest,
                          context) -> LastCommitForPathResponse:
        repo = self.load_repo(request.repository, context)
        revision, path = request.revision, request.path
        logger.debug("LastCommitForPath revision=%r, path=%r", revision, path)
        ctx = gitlab_revision_changeset(repo, revision)
        # gracinet: just hoping that performance wise, this does the right
        # thing, i.e do any scanning from the end
        # While we can be reasonably confident that the file exists
        # in the given revision, there are cases where deduplication implies
        # that the filelog() predicate would not see any new file revision
        # in some subgraph, because it's identical to another one that's not
        # in that subgraph. Hence using the slower `file` is the only way
        # to go.
        rev = repo.revs('file(%s) and ::%s', b'path:' + path, ctx).last()
        commit = None if rev is None else message.commit(repo[rev])
        return LastCommitForPathResponse(commit=commit)

    def ListLastCommitsForTree(self, request: ListLastCommitsForTreeRequest,
                               context) -> ListLastCommitsForTreeResponse:
        return not_implemented(context, ListLastCommitsForTreeResponse,
                               issue=14)  # pragma no cover

    def CommitsByMessage(self, request: CommitsByMessageRequest,
                         context) -> CommitsByMessageResponse:
        repo = self.load_repo(request.repository, context)
        query = request.query
        if not query:
            return CommitsByMessageResponse()
        pats = []
        opts = {}
        if request.path:
            path = repo.root + b'/' + request.path
            pats.append(path)
        if request.limit:
            opts[b'limit'] = request.limit
        if request.revision:
            revset = revset_from_gitlab_revision(repo, request.revision)
            if revset is None:
                logger.debug(
                    "CommitsByMessage revision %r could not be found",
                    request.revision)
                return CommitsByMessageResponse()
        else:
            revision = get_default_gitlab_branch(repo)
            # XXX: return error if no default branch found
            revset = revset_from_gitlab_revision(repo, revision)
        # Instead of sending 'query' as a key:value pair ('keyword': query) in
        # `opts`, appending the query to `revset` as "...and keyword('query')"
        # to make sure it perform an intersetion of two, instead of a union.
        revset = revset + b" and keyword('%b')" % query.encode()
        opts[b'rev'] = [revset]
        if util.versiontuple(n=2) <= (5, 5):  # hg<=5.5
            revs, _ = logcmdutil.getrevs(repo, pats, opts)
        else:  # hg>5.5
            walk_opts = logcmdutil.parseopts(repo.ui, pats, opts)
            revs, _ = logcmdutil.getrevs(repo, walk_opts)
        offset = request.offset
        if offset and offset > 0:
            revs = revs.slice(offset, len(revs))
        for chunk in chunked(revs):
            yield CommitsByMessageResponse(
                commits=(message.commit(repo[rev]) for rev in chunk))

    def ListCommitsByOid(self, request: ListCommitsByOidRequest,
                         context) -> ListCommitsByOidResponse:
        repo = self.load_repo(request.repository, context)
        lookup_error_classes = (error.LookupError, error.RepoLookupError)
        for chunk in chunked(pycompat.sysbytes(oid) for oid in request.oid):
            try:
                chunk_commits = [message.commit(repo[rev])
                                 for rev in repo.revs(b'%ls', chunk)]
            except lookup_error_classes:
                # lookup errors aren't surprising: the client uses this
                # method for prefix resolution
                # The reference Gitaly implementation tries them one after
                # the other (as of v13.4.6)
                chunk_commits = []
                for oid in chunk:
                    try:
                        # TODO here, something only involving the nodemap
                        # would be in order
                        revs = repo.revs(b'%s', oid)
                    except lookup_error_classes:
                        # ignore unresolvable oid prefix
                        pass
                    else:
                        if len(revs) == 1:
                            chunk_commits.append(
                                message.commit(repo[revs.first()]))
            yield ListCommitsByOidResponse(commits=chunk_commits)

    def ListCommitsByRefName(self, request: ListCommitsByRefNameRequest,
                             context) -> ListCommitsByRefNameResponse:
        repo = self.load_repo(request.repository, context)
        ref_names = request.ref_names

        commits = []
        for ref_name in ref_names:
            ctx = gitlab_revision_changeset(repo, ref_name)
            if ctx is None:
                logger.warning(
                    "ListCommitByRefName ref %r could not be "
                    "resolved to a changeset",
                    ref_name)
                continue
            commits.append([ref_name, ctx])
        CommitForRef = ListCommitsByRefNameResponse.CommitForRef
        for chunk in chunked(commits):
            yield ListCommitsByRefNameResponse(
                commit_refs=(CommitForRef(
                    commit=message.commit(ctx),
                    ref_name=ref_name
                ) for ref_name, ctx in chunk)
            )

    def FilterShasWithSignatures(self,
                                 request: FilterShasWithSignaturesRequest,
                                 context) -> FilterShasWithSignaturesResponse:
        return not_implemented(context, FilterShasWithSignaturesResponse,
                               issue=24)  # pragma no cover

    def GetCommitSignatures(self, request: GetCommitSignaturesRequest,
                            context) -> GetCommitSignaturesResponse:
        return not_implemented(context, GetCommitSignaturesResponse,
                               issue=24)  # pragma no cover

    def GetCommitMessages(self, request: GetCommitMessagesRequest,
                          context) -> GetCommitMessagesResponse:
        repo = self.load_repo(request.repository, context)
        results = {}
        for commit_id in request.commit_ids:
            commit_id = pycompat.sysbytes(commit_id)
            ctx = gitlab_revision_changeset(repo, commit_id)
            if ctx is None:
                # should not be an "internal" error, but
                # that's what Gitaly does anyway
                yield internal_error(
                    context, GetCommitMessagesResponse,
                    "failed to get commit message: object not found.",
                    log_level=logging.WARNING
                )
            results[commit_id] = ctx.description()
        for commit_id, msg in results.items():
            yield GetCommitMessagesResponse(commit_id=commit_id,
                                            message=msg)


def parse_find_commits_request_opts(request, repo):
    opts = {
        b'follow': request.follow,
        b'no_merges': request.skip_merges,
    }
    # TODO: implement 'request.first_parent' option
    # khanchi97: found that its counterpart follow-first in "hg log" is
    # deprecated and give wrong results with other options like revision,
    # all, etc.
    if request.limit:
        opts[b'limit'] = request.limit
    if request.author:
        opts[b'user'] = [request.author]
    after = request.after.ToSeconds()
    before = request.before.ToSeconds()
    date = getdate(after, before)
    if date is not None:
        opts[b'date'] = date

    revision = request.revision
    if request.all:
        opts[b'rev'] = [b'0:tip']
    elif not revision:
        revision = get_default_gitlab_branch(repo)
    if revision and not request.all:
        # `revision` and `all` are mutually exclusive,
        # if both present `all` gets the precedence
        revset = revset_from_gitlab_revision(repo, revision)
        opts[b'rev'] = [revset]
    return opts


def getdate(after, before):
    if after and before:
        after = _isoformat_from_seconds(after)
        before = _isoformat_from_seconds(before)
        return "%s UTC to %s UTC" % (after, before)
    elif after:
        after = _isoformat_from_seconds(after)
        return ">%s UTC" % after
    elif before:
        before = _isoformat_from_seconds(before)
        return "<%s UTC" % before
    return None


def _isoformat_from_seconds(secs):
    ts = Timestamp()
    ts.FromSeconds(int(secs))
    dt = ts.ToDatetime()
    return dt.isoformat()


def revset_from_gitlab_revision(repo, revision):
    """Find mercurial revset from a given GitLab revision.

    In theory, a GitLab revision could be any Git valid revspec, that
    we'd had to translate into its Mercurial counterpart.

    At this point, we only support most common git revision ranges, and
    a single revision.

    :return: the corresponding mercurial `revset`, or ``None`` if not found.
    """
    if b'...' in revision:
        #
        # r1...r2
        #    In git revspec, this implies csets ancestors of r1 or r2,
        #    but not ancestors of both
        #
        rev_start, rev_end = revision.split(b'...')
        if not rev_start:
            ctx_start = gitlab_revision_changeset(repo, b'HEAD')
        else:
            ctx_start = gitlab_revision_changeset(repo, rev_start)
        if not rev_end:
            ctx_end = gitlab_revision_changeset(repo, b'HEAD')
        else:
            ctx_end = gitlab_revision_changeset(repo, rev_end)
        left = ctx_start.rev()
        right = ctx_end.rev()
        branchpoint = repo.revs(b"ancestor(%d, %d)" % (left, right)).first()
        revset = b"(%d::%d | %d::%d) - %d" % (
            branchpoint, left, branchpoint, right, branchpoint
        )
        # sort them in descending order
        revset = b"sort(%s, -rev)" % revset
        return revset
    elif b'..' in revision:
        #
        # r1..r2
        #    In git revspec, this implies csets ancestors of r2, but not r1
        #
        # So the true Mercurial equivalent revset is actually `r2 % r1`.
        # Sadly, we happen to know `%` to be less efficient than DAG ranges.
        rev_start, rev_end = revision.split(b'..')
        if not rev_start:
            ctx_start = gitlab_revision_changeset(repo, b'HEAD')
        else:
            ctx_start = gitlab_revision_changeset(repo, rev_start)
        if not rev_end:
            ctx_end = gitlab_revision_changeset(repo, b'HEAD')
        else:
            ctx_end = gitlab_revision_changeset(repo, rev_end)
        revset = b"::%s - ::%s" % (ctx_end, ctx_start)
        # sort them in descending order
        revset = b"sort(%s, -rev)" % revset
        return revset
    else:
        ctx = gitlab_revision_changeset(repo, revision)
        if ctx is None:
            return None
        revset = b"reverse(::%s)" % ctx
        return revset
