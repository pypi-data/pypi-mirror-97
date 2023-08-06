# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from contextlib import contextmanager
from io import BytesIO
import grpc
import shutil
import tarfile

import pytest

from hgitaly.tests.common import make_empty_repo

from hgitaly.stub.repository_service_pb2 import (
    GetArchiveRequest,
    HasLocalBranchesRequest,
    RepositoryExistsRequest,
    WriteRefRequest,
)
from hgitaly.stub.repository_service_pb2_grpc import RepositoryServiceStub


def test_repository_exists(grpc_channel, server_repos_root):
    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    def exists(repo):
        return repo_stub.RepositoryExists(
            RepositoryExistsRequest(repository=repo)).exists

    assert exists(grpc_repo)

    # directory exists but is not a Mercurial repo
    shutil.rmtree(wrapper.path / '.hg')
    assert not exists(grpc_repo)

    # directory does not exist
    grpc_repo.relative_path = 'does/not/exist'
    assert not exists(grpc_repo)


def test_has_local_branches(grpc_channel, server_repos_root):
    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    def has_local_branches():
        return repo_stub.HasLocalBranches(
            HasLocalBranchesRequest(repository=grpc_repo)).value

    assert not has_local_branches()
    wrapper.write_commit('foo')
    assert has_local_branches()

    wrapper.command('commit', message=b"closing the only head!",
                    close_branch=True)

    assert not has_local_branches()


def test_write_ref(grpc_channel, server_repos_root):
    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    with pytest.raises(grpc.RpcError) as exc_info:
        repo_stub.WriteRef(WriteRefRequest(
            repository=grpc_repo,
            ref=b'refs/heads/something',
            revision=b'dead01234cafe'))
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    with pytest.raises(grpc.RpcError) as exc_info:
        repo_stub.WriteRef(WriteRefRequest(
            repository=grpc_repo,
            ref=b'HEAD',
            revision=b'topic/default/wont-last'))
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


@contextmanager
def get_archive_tarfile(stub, grpc_repo, commit_id, path=b''):
    with BytesIO() as fobj:
        for chunk_index, chunk_response in enumerate(
                stub.GetArchive(GetArchiveRequest(
                    repository=grpc_repo,
                    format=GetArchiveRequest.Format.Value('TAR'),
                    commit_id=commit_id,
                    path=path,
                    prefix='archive-dir',
                ))):
            fobj.write(chunk_response.data)

        fobj.seek(0)
        with tarfile.open(fileobj=fobj) as tarf:
            yield tarf, chunk_index + 1


def test_get_archive(grpc_channel, server_repos_root, tmpdir):
    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    ctx = wrapper.write_commit('foo', content="Foo")
    (wrapper.path / 'sub').mkdir()
    ctx2 = wrapper.write_commit('sub/bar', content="Bar")

    node_str = ctx.hex().decode()
    with get_archive_tarfile(repo_stub, grpc_repo, node_str) as (tarf, _nb):
        assert set(tarf.getnames()) == {'archive-dir/.hg_archival.txt',
                                        'archive-dir/foo'}

        extract_dir = tmpdir.join('extract')
        tarf.extractall(path=extract_dir)

        metadata_lines = extract_dir.join('archive-dir',
                                          '.hg_archival.txt').readlines()

        assert 'node: %s\n' % node_str in metadata_lines
        assert extract_dir.join('archive-dir', 'foo').read() == "Foo"

    node2_str = ctx2.hex().decode()
    with get_archive_tarfile(repo_stub, grpc_repo, node2_str) as (tarf, _nb):
        assert set(tarf.getnames()) == {'archive-dir/.hg_archival.txt',
                                        'archive-dir/foo',
                                        'archive-dir/sub/bar'}

        extract_dir = tmpdir.join('extract-2')
        tarf.extractall(path=extract_dir)

        metadata_lines = extract_dir.join('archive-dir',
                                          '.hg_archival.txt').readlines()

        assert 'node: %s\n' % node2_str in metadata_lines
        assert extract_dir.join('archive-dir', 'sub', 'bar').read() == "Bar"

    with get_archive_tarfile(
            repo_stub, grpc_repo, node2_str, path=b'sub') as (tarf, _nb):
        assert tarf.getnames() == ['archive-dir/sub/bar']

        extract_dir = tmpdir.join('extract-sub')
        tarf.extractall(path=extract_dir)
        assert extract_dir.join('archive-dir', 'sub', 'bar').read() == "Bar"

    with pytest.raises(grpc.RpcError) as exc_info:
        get_archive_tarfile(
            repo_stub, grpc_repo, node2_str,
            path=b'/etc/passwd'
        ).__enter__()  # needed to actually perform the RPC call
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_get_archive_multiple_chunks(grpc_channel, server_repos_root,
                                     tmpdir, monkeypatch):

    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    # we can't just override the environment variable: it's read at module
    # import time.
    large_content = "Foo" * 200000
    ctx = wrapper.write_commit('foo', content=large_content)
    node_str = ctx.hex().decode()
    with get_archive_tarfile(repo_stub, grpc_repo, node_str) as (tarf, count):
        assert count > 1
        assert set(tarf.getnames()) == {'archive-dir/.hg_archival.txt',
                                        'archive-dir/foo'}

        extract_dir = tmpdir.join('extract')
        tarf.extractall(path=extract_dir)

        metadata_lines = extract_dir.join('archive-dir',
                                          '.hg_archival.txt').readlines()

        assert 'node: %s\n' % node_str in metadata_lines
        assert extract_dir.join('archive-dir', 'foo').read() == large_content

    del large_content
