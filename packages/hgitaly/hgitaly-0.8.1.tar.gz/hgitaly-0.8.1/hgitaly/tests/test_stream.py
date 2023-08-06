# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import os

from .. import stream


def test_env_write_buffer_size(monkeypatch):
    monkeypatch.setitem(os.environ, 'GITALY_STREAMIO_WRITE_BUFFER_SIZE', '12')

    assert stream.env_write_buffer_size() == 12
