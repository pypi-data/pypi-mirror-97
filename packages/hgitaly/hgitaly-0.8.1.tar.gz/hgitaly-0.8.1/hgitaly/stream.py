# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later

# Quoting from Gitaly 13.4:
# //  WriteBufferSize is the largest []byte that Write() will pass
# //  to its underlying send function. This value can be changed
# //  at runtime using the GITALY_STREAMIO_WRITE_BUFFER_SIZE environment
# //  variable.
#
# var WriteBufferSize = 128 * 1024
#
# As of GitLab 13.4, the environment variable is parsed with
# `strconv.ParseInt(value, 0, 32)`.
# Quoting https://golang.org/pkg/strconv/#ParseInt:
#     If the base argument is 0, the true base is implied by
#     the string's prefix: 2 for "0b", 8 for "0" or "0o", 16 for "0x",
#     and 10 otherwise. Also, for argument base 0 only,
#     underscore characters are permitted as defined by the
#     Go syntax for integer literals.
import os


def parse_int(s):
    """Parse integer string representations, as Golangs `strconf.ParseInt`

    # TODO check at least octal and hex syntaxes
    >>> parse_int('10')
    10
    """
    return int(s)


def env_write_buffer_size():
    str_val = os.environ.get('GITALY_STREAMIO_WRITE_BUFFER_SIZE')
    if not str_val:
        return 128 * 1024
    return parse_int(str_val)


WRITE_BUFFER_SIZE = env_write_buffer_size()
