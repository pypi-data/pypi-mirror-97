# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
The module accessible within pybuilds

Note that this module should not be imported outside of pybuild files
"""

import portmod.globals  # noqa  # pylint: disable=unused-import
from portmod.atom import version_gt  # noqa  # pylint: disable=unused-import
from portmod.fs.util import patch_dir  # noqa  # pylint: disable=unused-import
from portmod.masters import get_masters  # noqa  # pylint: disable=unused-import
from portmod.parsers.usestr import use_reduce  # noqa  # pylint: disable=unused-import
from portmod.vfs import find_file, list_dir  # noqa  # pylint: disable=unused-import

from .pybuild import (  # noqa  # pylint: disable=unused-import
    File,
    InstallDir,
    Pybuild1,
    apply_patch,
)

DOWNLOAD_DIR = portmod.globals.env.DOWNLOAD_DIR

__all__ = [
    "version_gt",
    "patch_dir",
    "get_masters",
    "use_reduce",
    "find_file",
    "list_dir",
    "File",
    "InstallDir",
    "Pybuild1",
    "apply_patch",
    "DOWNLOAD_DIR",
]
