# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import logging
import os

from grpc import StatusCode
from mercurial import (
    error,
    hg,
    ui as uimod,
)
from .stub.shared_pb2 import (
    Repository,
)

logger = logging.getLogger(__name__)


class HGitalyServicer:
    """Common features of all HGitaly services.

    Attributes:

    - :attr:`storages`: a :class:`dict` mapping storage names to corresponding
      root directory absolute paths, which are given as bytes since we'll have
      to convert paths to bytes anyway, which is the only promise a filesystem
      can make, and what Mercurial expects.
    - :attr:`ui`: base :class:`mercurial.ui.ui` instance from which repository
      uis are derived. In particular, it bears the common configuration.
    """

    def __init__(self, storages):
        self.storages = storages
        self.ui = uimod.ui.load()

    def load_repo(self, repository: Repository, context):
        """Load the repository from storage name and relative path

        :param repository: Repository Gitaly Message, encoding storage name
            and relative path
        :param context: gRPC context (used in error raising)
        :raises: ``KeyError('storage', storage_name)`` if storage is not found.

        Error treatment: the caller doesn't have to do anything specific,
        the status code and the details are already set in context, and these
        are automatically propagated to the client (see corresponding test
        in `test_servicer.py`). Still, the caller can still catch the
        raised exception and change the code and details as they wish.
        """
        # shamelessly taken from heptapod.wsgi for the Hgitaly bootstrap
        # note that Gitaly Repository has more than just a relative path,
        # we'll have to decide what we make of the extra information
        rpath = repository.relative_path
        if rpath.endswith('.git'):
            rpath = rpath[:-4] + '.hg'

        root_dir = self.storages.get(repository.storage_name)
        if root_dir is None:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details(
                "No storage named %r" % repository.storage_name)
            raise KeyError('storage', repository.storage_name)

        # GitLab filesystem paths are always ASCII
        repo_path = os.path.join(root_dir, rpath.encode('ascii'))
        logger.info("loading repo at %r", repo_path)

        # ensure caller gets private copy of ui
        try:
            return hg.repository(self.ui.copy(), repo_path)
        except error.RepoError as exc:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details(repr(exc.args))
            raise KeyError('repo', repo_path)
