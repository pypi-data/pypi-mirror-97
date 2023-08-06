# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from grpc import StatusCode
import logging
import tempfile

from mercurial import (
    archival,
    scmutil,
)

# TODO move that to the heptapod package
from hgext3rd.heptapod.git import git_branch_from_ref

from ..errors import (
    not_implemented,
)
from ..branch import (
    iter_gitlab_branches,
)
from ..stub.repository_service_pb2 import (
    RepositoryExistsRequest,
    RepositoryExistsResponse,
    GetArchiveRequest,
    GetArchiveResponse,
    HasLocalBranchesRequest,
    HasLocalBranchesResponse,
    WriteRefRequest,
    WriteRefResponse,
    ApplyGitattributesRequest,
    ApplyGitattributesResponse,
)
from ..stub.repository_service_pb2_grpc import RepositoryServiceServicer
from ..servicer import HGitalyServicer
from ..stream import WRITE_BUFFER_SIZE
from ..path import (
    InvalidPath,
    validate_relative_path,
)


logger = logging.getLogger(__name__)
DEFAULT_BRANCH_FILE_NAME = b'default_gitlab_branch'
ARCHIVE_FORMATS = {
    GetArchiveRequest.Format.Value('ZIP'): b'zip',
    GetArchiveRequest.Format.Value('TAR'): b'tar',
    GetArchiveRequest.Format.Value('TAR_GZ'): b'tgz',
    GetArchiveRequest.Format.Value('TAR_BZ2'): b'tbz2',
}


class RepositoryServiceServicer(RepositoryServiceServicer, HGitalyServicer):
    """RepositoryServiceService implementation.
    """

    def RepositoryExists(self,
                         request: RepositoryExistsRequest,
                         context) -> RepositoryExistsResponse:
        try:
            self.load_repo(request.repository, context)
            exists = True
        except KeyError:
            exists = False
            # TODO would be better to have a two-layer helper
            # in servicer: load_repo() for proper gRPC error handling and
            # load_repo_raw_exceptions() (name to be improved) to get the
            # raw exceptions
            context.set_code(StatusCode.OK)
            context.set_details('')

        return RepositoryExistsResponse(exists=exists)

    def GetArchive(self,
                   request: GetArchiveRequest,
                   context) -> GetArchiveResponse:
        logger.debug("GetArchive request=%r", request)
        repo = self.load_repo(request.repository, context)
        ctx = repo[request.commit_id]

        patterns = []
        path = request.path
        if path:
            try:
                path = validate_relative_path(repo, path)
            except InvalidPath:
                context.set_code(StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid path: '%s'" % path)
                return GetArchiveResponse()
            patterns.append(b"path:" + path)

        match = scmutil.match(ctx, pats=patterns, opts={})

        # using an anonymous (not linked) temporary file
        # TODO OPTIM check if archive is not by any chance
        # using a tempfile already…
        with tempfile.TemporaryFile(
                mode='wb+',  # the default, but let's insist on binary here
                buffering=WRITE_BUFFER_SIZE) as tmpf:
            archival.archive(
                repo,
                tmpf,
                ctx.node(),
                ARCHIVE_FORMATS[request.format],
                True,  # decode (TODO this is the default but what is this?)
                match,
                request.prefix.encode(),
                subrepos=False  # maybe later, check what GitLab's standard is
            )

            tmpf.seek(0)
            while True:
                data = tmpf.read(WRITE_BUFFER_SIZE)
                if not data:
                    break
                yield GetArchiveResponse(data=data)

    def HasLocalBranches(self,
                         request: HasLocalBranchesRequest,
                         context) -> HasLocalBranchesResponse:
        repo = self.load_repo(request.repository, context)
        # the iteration should stop as soon at first branchmap entry which
        # has a non closed head (but all heads in that entry would be checked
        # to be non closed)
        return HasLocalBranchesResponse(value=any(iter_gitlab_branches(repo)))

    def WriteRef(
            self,
            request: WriteRefRequest,
            context) -> WriteRefResponse:
        if request.ref != b'HEAD':
            context.set_code(StatusCode.INVALID_ARGUMENT)
            context.set_details(
                "Moving a GitLab branch is not implemented in Mercurial "
                "and would at most make sense for bookmarks.")
            return WriteRefResponse()

        target = git_branch_from_ref(request.revision)
        if target is None:
            context.set_code(StatusCode.INVALID_ARGUMENT)
            context.set_details(
                "The default GitLab branch can only be set "
                "to a branch ref, got %r" % request.revision)
            return WriteRefResponse()

        repo = self.load_repo(request.repository, context)
        # TODO that part and the constant should go to hgext3rd.heptapod, since
        # the default branch will have to be set by push reception.
        with repo.wlock():
            repo.vfs.write(DEFAULT_BRANCH_FILE_NAME, target)
        return WriteRefResponse()

    def ApplyGitattributes(self, request: ApplyGitattributesRequest,
                           context) -> ApplyGitattributesResponse:
        """Method used as testing bed for the `not_implemented` helper.

        It is unlikely we ever implement this one, and if we do something
        similar, we'll probably end up defining a ApplyHgAttributes anyway.
        """
        return not_implemented(context, ApplyGitattributesResponse,
                               issue=1234567)
