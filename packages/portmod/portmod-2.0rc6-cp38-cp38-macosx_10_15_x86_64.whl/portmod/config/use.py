# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import re
from functools import lru_cache
from logging import info, warning
from typing import Optional, Set, Tuple, cast

from portmod.atom import Atom
from portmod.functools import prefix_aware_cache
from portmod.globals import env
from portmod.l10n import l10n
from portmod.parsers.flags import add_flag, collapse_flags, get_flags, remove_flag
from portmod.parsers.usestr import use_reduce
from portmod.pybuild import Pybuild
from portmod.repo.profiles import profile_parents

from . import get_config, read_config, set_config_value
from .textures import select_texture_size


class InvalidFlag(Exception):
    """Exception indicating an invalid use flag"""

    def __init__(self, flag: str, atom: Optional[Atom] = None):
        if atom:
            super().__init__(l10n("invalid-flag-atom", flag=flag, atom=atom))
        else:
            super().__init__(l10n("invalid-flag", flag=flag))


@lru_cache(maxsize=None)
def get_use_expand_flags() -> Set[str]:
    """Returns all currently enabled USE_EXPAND flags"""
    flags = set()
    for use in get_config().get("USE_EXPAND", []):
        if not use.startswith("-"):
            for flag in get_config().get(use, "").split():
                flags.add(f"{use.lower()}_{flag}")
    return flags


def get_use_expand(pkg: Pybuild, use_expand: str) -> Tuple[Set[str], Set[str]]:
    """
    Returns the set of enabled flags for the given package and USE_EXPAND category
    """
    flags = {
        re.sub(f"^{use_expand.lower()}_", "", flag)
        for flag in pkg.IUSE_EFFECTIVE
        if flag.startswith(f"{use_expand.lower()}_")
    }
    enabled_use = pkg.get_enabled_use()
    enabled_expand = {
        re.sub(f"^{use_expand}_", "", val, flags=re.IGNORECASE)
        for val in enabled_use
        if val.startswith(use_expand.lower() + "_")
    }

    return enabled_expand, flags - enabled_expand


@prefix_aware_cache
def get_user_global_use() -> Set[str]:
    """Returns user-specified global use flags"""
    global_use = cast(
        Set[str], read_config(env.prefix().PORTMOD_CONFIG, {}).get("USE", set())
    )

    # Also return global user-set USE_EXPAND values
    for use in get_config().get("USE_EXPAND", []):
        values = set(read_config(env.prefix().PORTMOD_CONFIG, {}).get(use, "").split())
        flags = {use.lower() + "_" + value for value in values}
        global_use |= flags

    return global_use


@prefix_aware_cache
def get_user_use(atom: Atom) -> Set[str]:
    """Returns user-specified use flags for a given mod"""
    use_file = os.path.join(env.prefix().PORTMOD_CONFIG_DIR, "package.use")
    if os.path.exists(use_file):
        return get_flags(use_file, atom)

    return set()


@prefix_aware_cache
def get_forced_use(atom: Atom) -> Set[str]:
    """Returns a list of forced use flags for the given mod"""
    force: Set[str] = set()
    for parent_dir in profile_parents():
        force_file = os.path.join(parent_dir, "use.force")
        if os.path.exists(force_file):
            flags = get_flags(force_file)
            force = collapse_flags(force, flags)

        mod_force_file = os.path.join(parent_dir, "package.use.force")
        if os.path.exists(mod_force_file):
            flags = get_flags(mod_force_file, atom)
            force = collapse_flags(force, flags)

    return force


@prefix_aware_cache
def get_use(mod: Pybuild) -> Tuple[Set[str], Set[str]]:
    """Returns a list of enabled and a list of disabled use flags"""
    GLOBAL_USE = get_config().get("USE", [])
    use: Set[str] = get_use_expand_flags()
    use = collapse_flags(use, GLOBAL_USE)
    for parent_dir in profile_parents():
        use_file = os.path.join(parent_dir, "package.use")
        if os.path.exists(use_file):
            flags = get_flags(use_file, mod.ATOM)
            use = collapse_flags(use, flags)

    # User config is the last added, overriding profile flags
    use = collapse_flags(use, get_user_use(mod.ATOM))

    # Finally, apply environment variables (technically, we do this twice,
    # as GLOBAL_USE also includes these, but we need to apply them again to
    # ensure they override
    use = collapse_flags(use, os.environ.get("USE", []))

    # Forced use flags must be collapsed last to ensure that the
    # forced flags override any other values
    use = collapse_flags(use, get_forced_use(mod.ATOM))

    enabled_use = {x for x in use if not x.startswith("-")}
    disabled_use = {x.lstrip("-") for x in use if x.startswith("-")}

    enabled_use = enabled_use.intersection(mod.IUSE_EFFECTIVE) | {
        x.lstrip("+")
        for x in mod.IUSE
        if x.startswith("+") and x.lstrip("+") not in disabled_use
    }

    disabled_use = disabled_use.intersection(mod.IUSE_EFFECTIVE)

    texture_sizes = use_reduce(
        mod.TEXTURE_SIZES, enabled_use, disabled_use, token_class=int
    )
    texture_size = select_texture_size(texture_sizes)
    if texture_size is not None:
        found = None
        for useflag in enabled_use:
            if useflag.startswith("texture_size_"):
                if not found:
                    found = useflag
                elif useflag != found:
                    raise Exception(
                        l10n(
                            "multiple-texture-flags",
                            flag1=use,
                            flag2=found,
                            atom=mod.ATOM,
                        )
                    )
        enabled_use.add(found or "texture_size_{}".format(texture_size))

    return (enabled_use, disabled_use)


def verify_use(flag: str, atom: Optional[Atom] = None) -> bool:
    """
    Verifies that the given flag is valid

    args:
        flag: Flag to be added
        atom: If present, checks for local use flags relevant to this atom.
              Otherwise, global use flags will be considered
    returns:
        Whether or not the use flag is valid given either the atom passed,
        or the global context
    """
    from portmod.repo.metadata import get_global_use

    from ..loader import load_pkg

    if atom:
        return any(flag in mod.IUSE_EFFECTIVE for mod in load_pkg(atom))
    else:
        return flag in [
            flag
            for repo in env.prefix().REPOS
            for flag in get_global_use(repo.location)
        ]


def add_use(flag: str, atom: Optional[Atom] = None, disable: bool = False):
    """
    Adds the given use flag to the user's configuration

    Args:
        flag: Flag to be added
        atom: If present, the flag will only apply to this package
        disable: If True, the flag is added in its disabled form (prefixed with "-")
    """
    from portmod.loader import load_pkg

    if disable and flag in get_config().get("USE", []):
        remove_use(flag, atom)

    disableflag = "-" + flag

    if (disable and flag in get_config().get("USE", [])) or (
        not disable and disableflag in get_config().get("USE", [])
    ):
        remove_use(flag, atom)

    if not verify_use(flag, atom):
        if atom:
            raise InvalidFlag(flag, atom)
        else:
            raise InvalidFlag(flag)
        return

    if atom is not None:
        from portmod.util import select_package

        (newest, req) = select_package(load_pkg(atom))
        if flag not in newest.IUSE_EFFECTIVE:
            warning(
                l10n(
                    "invalid-use-flag-warning", flag=flag, atom1=newest.ATOM, atom2=atom
                )
            )

    if atom:
        use_file = os.path.join(env.prefix().PORTMOD_CONFIG_DIR, "package.use")
        if disable:
            remove_flag(use_file, atom, flag)
            add_flag(use_file, atom, disableflag)
        else:
            remove_flag(use_file, atom, disableflag)
            add_flag(use_file, atom, flag)
        get_user_use.cache_clear()  # type: ignore
    else:
        GLOBAL_USE = get_config()["USE"]

        if (not disable and flag not in GLOBAL_USE) or (
            disable and disableflag not in GLOBAL_USE
        ):
            if disable:
                info(l10n("adding-use-flag", flag="-" + flag))
                GLOBAL_USE.add(disableflag)
            else:
                info(l10n("adding-use-flag", flag=flag))
                GLOBAL_USE.add(flag)

            set_config_value("USE", " ".join(sorted(GLOBAL_USE)))
            get_user_global_use.cache_clear()  # type: ignore
        else:
            if disable:
                warning(l10n("global-use-flag-already-disabled", flag=flag))
            else:
                warning(l10n("global-use-flag-already-enabled", flag=flag))
    get_use.cache_clear()  # type: ignore


def remove_use(flag: str, atom: Optional[Atom] = None):
    """
    Removes the given use flag from the user's configuration

    This will remove both enabled and disabled flags

    Args:
        flag: Flag to be removed
        atom: If present, the flag will only be removed from configuration specifically
              affecting this package atom
    """

    disableflag = "-" + flag

    if not verify_use(flag, atom):
        warning(l10n("invalid-flag-atom", flag=flag, atom=atom))

    if atom is not None:
        use_file = os.path.join(env.prefix().PORTMOD_CONFIG_DIR, "package.use")
        remove_flag(use_file, atom, flag)
        remove_flag(use_file, atom, disableflag)
        get_user_use.cache_clear()  # type: ignore
    else:
        GLOBAL_USE = get_config()["USE"]

        if flag in GLOBAL_USE or disableflag in GLOBAL_USE:
            if flag in GLOBAL_USE:
                info(l10n("removing-use-flag", flag=flag))
                GLOBAL_USE.remove(flag)

            if disableflag in GLOBAL_USE:
                info(l10n("removing-use-flag", flag="-" + flag))
                GLOBAL_USE.remove(disableflag)

            set_config_value("USE", " ".join(sorted(GLOBAL_USE)))
            get_user_global_use.cache_clear()  # type: ignore
        else:
            warning(l10n("flag-not-set-globally", flag=flag))
    get_use.cache_clear()  # type: ignore
