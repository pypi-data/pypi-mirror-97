# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later

from heptapod.testhelpers import (
    LocalRepoWrapper,
)
from ..revision import (
    gitlab_revision_changeset,
)


def make_repo(path):
    return LocalRepoWrapper.init(path,
                                 config=dict(
                                     extensions=dict(topic='', evolve=''),
                                 ))


def test_gitlab_revision_changeset_by_hex(tmpdir):
    wrapper = make_repo(tmpdir)
    repo = wrapper.repo

    ctx = wrapper.write_commit('foo')

    assert gitlab_revision_changeset(repo, ctx.hex()) == ctx

    wrapper.command('amend', message=b'amended')

    obs_ctx = gitlab_revision_changeset(repo, ctx.hex())
    assert obs_ctx == ctx
    assert obs_ctx.obsolete()


def test_gitlab_revision_gl_branch(tmpdir):
    wrapper = make_repo(tmpdir)
    repo = wrapper.repo
    ctx = wrapper.write_commit('foo')

    assert (
        gitlab_revision_changeset(repo, b'refs/heads/branch/default')
        == ctx
    )
    assert gitlab_revision_changeset(repo, b'branch/default') == ctx

    # precise ref form can be for nothing but a branch
    # here, just stripping the prefix would end over to direct lookup by
    # tag, bookmark or node ID
    assert gitlab_revision_changeset(repo, b'refs/heads/' + ctx.hex()) is None
