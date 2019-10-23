# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2017-2019 Jani Nikula <jani@nikula.org>

"""
Late, another terrible excuse.

An RFC5545 iCalendar search and manipulation tool.
"""

import os

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'VERSION')) as version_file:
    __version__ = version_file.read().strip()
