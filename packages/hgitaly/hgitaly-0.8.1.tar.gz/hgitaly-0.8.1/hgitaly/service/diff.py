# Copyright 2021 Sushil Khanchi <sushilkhanchi97@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging

from ..errors import (
    not_implemented,
)
from ..stub.diff_pb2 import (
    CommitDiffRequest,
    CommitDiffResponse,
    CommitDeltaRequest,
    CommitDeltaResponse,
    RawDiffRequest,
    RawDiffResponse,
    RawPatchRequest,
    RawPatchResponse,
    DiffStatsRequest,
    DiffStatsResponse,
)
from ..stub.diff_pb2_grpc import DiffServiceServicer

from ..servicer import HGitalyServicer

logger = logging.getLogger(__name__)


class DiffServicer(DiffServiceServicer, HGitalyServicer):
    """DiffService implementation.

    The ordering of methods in this source file is the same as in the proto
    file.
    """
    def CommitDiff(self, request: CommitDiffRequest,
                   context) -> CommitDiffResponse:
        return not_implemented(context, CommitDiffResponse,
                               issue=38)  # pragma no cover

    def CommitDelta(self, request: CommitDeltaRequest,
                    context) -> CommitDeltaResponse:
        return not_implemented(context, CommitDeltaResponse,
                               issue=39)  # pragma no cover

    def RawDiff(self, request: RawDiffRequest,
                context) -> RawDiffResponse:
        return not_implemented(context, RawDiffResponse,
                               issue=40)  # pragma no cover

    def RawPatch(self, request: RawPatchRequest,
                 context) -> RawPatchResponse:
        return not_implemented(context, RawPatchResponse,
                               issue=41)  # pragma no cover

    def DiffStats(self, request: DiffStatsRequest,
                  context) -> DiffStatsResponse:
        return not_implemented(context, DiffStatsResponse,
                               issue=42)  # pragma no cover
