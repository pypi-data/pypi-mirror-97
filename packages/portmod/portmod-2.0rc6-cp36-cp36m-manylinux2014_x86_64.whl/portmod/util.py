# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Various utility functions
"""

import fnmatch
import os
import re
from collections import namedtuple
from typing import Any, Iterable, List, Optional, Pattern, Tuple, Union

from portmod.config.license import has_eula, is_license_accepted
from portmod.repo.keywords import accepts, accepts_testing, get_keywords

from .atom import version_gt
from .config import get_config
from .globals import env
from .pybuild import Pybuild

KeywordDep = namedtuple("KeywordDep", ["atom", "keyword"])
LicenseDep = namedtuple("LicenseDep", ["atom", "license", "is_eula"])


def get_keyword_dep(package: Pybuild) -> Optional[KeywordDep]:
    if not accepts(get_keywords(package.ATOM), package.KEYWORDS):
        arch = env.prefix().ARCH
        if accepts_testing(arch, package.KEYWORDS):
            return KeywordDep(package.ATOM.CP, "~" + arch)
        return KeywordDep("=" + package.ATOM.CP, "**")
    return None


def select_package(packages: Iterable[Pybuild]) -> Tuple[Pybuild, Any]:
    """
    Chooses a mod version based on keywords and accepts it if the license is accepted
    """
    if not packages:
        raise Exception("Cannot select mod from empty modlist")

    filtered = list(
        filter(lambda pkg: accepts(get_keywords(pkg.ATOM), pkg.KEYWORDS), packages)
    )

    keyword = None

    if filtered:
        mod = get_newest(filtered)
    else:
        arch = env.prefix().ARCH
        # No mods were accepted. Choose the best version and add the keyword
        # as a requirement for it to be installed
        unstable = list(
            filter(lambda mod: accepts_testing(arch, mod.KEYWORDS), packages)
        )
        if unstable:
            mod = get_newest(unstable)
            keyword = "~" + arch
        else:
            # There was no mod that would be accepted by enabling testing.
            # Try enabling unstable
            mod = get_newest(packages)
            keyword = "**"

    if not is_license_accepted(mod):
        return (mod, LicenseDep(mod.CPN, mod.LICENSE, has_eula(mod)))
    if keyword is not None:
        return (mod, KeywordDep("=" + mod.ATOM.CPF, keyword))

    return (mod, None)


def get_max_version(versions: Iterable[str]) -> Optional[str]:
    """
    Returns the largest version in the given list

    Version should be a valid version according to PMS section 3.2,
    optionally follwed by a revision

    Returns None if the version list is empty
    """
    newest = None
    for version in versions:
        if newest is None or version_gt(version, newest):
            newest = version
    return newest


def get_newest(packages: Iterable[Pybuild]) -> Pybuild:
    """
    Returns the newest mod in the given list based on version
    If there is a tie, returns the earlier mod in the list
    """
    max_ver = get_max_version([pkg.PVR for pkg in packages])
    for pkg in packages:
        if pkg.PVR == max_ver:
            return pkg
    raise Exception(
        f"Internal Error: get_max_version returned incorrect result {max_ver}"
    )


def fnmatch_list_to_re(patterns: List[str]) -> Pattern:
    def to_re(value: Union[str, Pattern]):
        """
        Converts fn-match string into a regular expression string

        Note that normpath may not work as expected with fn-match strings
        if forward-slashes are present inside bracketed ranges (e.g. [/../]).
        """
        if isinstance(value, Pattern):
            return value
        return fnmatch.translate(os.path.normpath(value))

    flags = 0
    if get_config().get("CASE_INSENSITIVE_FILES", False):
        flags = re.IGNORECASE
    return re.compile("|".join(map(to_re, patterns)), flags=flags)
