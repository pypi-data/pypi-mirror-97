# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import grpc
import pytest
from mercurial import pycompat

from heptapod.testhelpers import (
    LocalRepoWrapper,
)

from ..servicer import HGitalyServicer
from ..stub.shared_pb2 import (
    Repository,
)
from ..stub.repository_service_pb2 import HasLocalBranchesRequest
from ..stub.repository_service_pb2_grpc import RepositoryServiceStub


class FakeContext:

    def set_code(self, code):
        self.code = code

    def set_details(self, details):
        self.details = details


def test_load_repo(tmpdir):
    storage_root = tmpdir.join('repos')
    storage_root_bytes = pycompat.sysbytes(str(storage_root))
    servicer = HGitalyServicer(dict(storname=storage_root_bytes))
    # context is used for error raising only
    context = FakeContext()

    wrapper = LocalRepoWrapper.init(storage_root.join('awesome-proj.hg'))
    loaded = servicer.load_repo(Repository(storage_name='storname',
                                           relative_path='awesome-proj.hg'),
                                context)
    assert loaded.root == wrapper.repo.root

    # In practice, requests from the Rails app will assume the relevant
    # path to end in `.git`, we need to ignore that.
    loaded = servicer.load_repo(Repository(storage_name='storname',
                                           relative_path='awesome-proj.git'),
                                context)
    assert loaded.root == wrapper.repo.root

    with pytest.raises(KeyError) as exc_info:
        servicer.load_repo(Repository(storage_name='dream',
                                      relative_path='dream-proj.hg'),
                           context)
    assert exc_info.value.args == ('storage', 'dream')
    assert context.code == grpc.StatusCode.NOT_FOUND


def test_not_found_propagation(grpc_channel, server_repos_root):
    # Taking a random RPC to check that the client receives the
    # proper error response
    repo_stub = RepositoryServiceStub(grpc_channel)

    with pytest.raises(grpc.RpcError) as exc_info:
        repo_stub.HasLocalBranches(HasLocalBranchesRequest(
            repository=Repository(storage_name='dream', relative_path='')))
    exc = exc_info.value

    assert exc.code() == grpc.StatusCode.NOT_FOUND
    assert 'dream' in exc.details()

    with pytest.raises(grpc.RpcError) as exc_info:
        repo_stub.HasLocalBranches(HasLocalBranchesRequest(
            repository=Repository(storage_name='default',
                                  relative_path='not_here')))
    exc = exc_info.value

    assert exc.code() == grpc.StatusCode.NOT_FOUND
    assert 'not_here' in exc.details()
