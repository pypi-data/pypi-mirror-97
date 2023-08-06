# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from functools import cmp_to_key
from types import SimpleNamespace
from typing import AbstractSet, Iterable, Mapping

from portmod.atom import Atom, FQAtom, QualifiedAtom, version_gt
from portmod.config.sets import is_selected
from portmod.config.use import get_use, get_user_global_use, get_user_use
from portmod.loader import load_all_installed, load_installed_pkg, load_pkg, load_pkg_fq
from portmod.repo import get_repo
from portmod.util import get_keyword_dep

from .formula import Formula

WEIGHTS = SimpleNamespace()

###################################################################################
WEIGHTS.base_update = 1  # Base weight for the lowest
WEIGHTS.update_diff = 10  # Difference between each update, in order
# Weight to keep mods that are installed, but not selected
# The negative of this is set if depclean is enabled (plus total_up_weight)
WEIGHTS.keep_installed = 2
# Weight to keep a mod that is not selected and not installed disabled
WEIGHTS.not_needed = 2
WEIGHTS.user_flag = 4  # Weight to keep a user-set flag the same
WEIGHTS.default_flag = 3  # Weight to keep a flag at its default value
###################################################################################


def weigh_clauses(
    atoms: Mapping[QualifiedAtom, Iterable[FQAtom]],
    flags: Iterable[FQAtom],
    explicit: AbstractSet[Atom],
    *,
    deep: bool,
    depclean: bool,
    update: bool,
    newuse: bool,
) -> Formula:
    """Creates soft clauses for the given atoms"""
    formula = Formula()
    # Soft clauses to minimize unwanted changes to user's configuration

    # Track total weights so that we can make sure that higher-priority clauses
    # always have a greater weight
    total_up_weight = 0
    total_not_needed = 0

    # Clause for each mod not installed, with a small weight penalty for installing them
    for group in formula.atoms:
        for atom in formula.atoms[group]:
            if (
                not load_installed_pkg(Atom(atom.CPN))
                and not is_selected(atom)
                and Atom(atom.CPN) not in explicit
            ):
                formula.append(["-" + atom], weight=WEIGHTS.not_needed)
                total_not_needed += WEIGHTS.not_needed

    flag_formula, total_flag_weight = weigh_flags(flags, explicit, newuse=newuse)
    formula.merge(flag_formula)

    # Ensure that the update weight is at least greater than the total number of packages to
    # overcome the basic resistance against moving from an installed package to the repository's
    # version of that installed package (i.e. rebuilding)
    total_atoms = sum(len(group) for group in atoms)

    # Penalize out of date versions.
    for group in atoms:
        # Divide mods into stable, testing and unstable
        # If user accepts testing keywords, they will be considered stable
        stable = set()
        testing = set()
        unstable = set()
        for atom in atoms[group]:
            mod = load_pkg_fq(atom)
            keyword = get_keyword_dep(mod)
            if not keyword:
                stable.add(atom)
            elif keyword.keyword.startswith("~"):
                testing.add(atom)
            elif keyword.keyword == "**":
                unstable.add(atom)

        i = WEIGHTS.base_update
        inc = WEIGHTS.update_diff + total_flag_weight

        def cmp(x, y):
            (vx, rx, ax) = x
            (vy, ry, ay) = y
            # Atoms are sorted first by version, then repo priority.
            # The installed Repo (here represented by None) has the
            # lowest priority
            if version_gt(vx, vy):
                return -1
            elif not version_gt(vy, vx):
                # If nether is greater than the other, they are equal
                # The installed version comes first, unless the package was selected
                if atom.CPN in explicit:
                    if rx is None:
                        return 1
                    if ry is None:
                        return -1
                else:
                    if rx is None:
                        return -1
                    if ry is None:
                        return 1
                if rx.priority > ry.priority:
                    return -1
            return 1

        def weigh(li):
            nonlocal i, total_up_weight
            tosort = []
            for atom in li:
                if atom.R.endswith("::installed") or atom.R == "installed":
                    repo = None
                else:
                    repo = get_repo(atom.R)
                tosort.append((atom.PVR, repo, atom))

            inorder = sorted(tosort, key=cmp_to_key(cmp))
            for index, (version, repo, atom) in enumerate(inorder):
                formula.append(["-" + atom], weight=i)
                if (
                    index < len(inorder) - 1
                    and inorder[index + 1][0] == version
                    and repo is None
                ):
                    # This version is installed
                    # The weight difference between installed and non-installed should be exactly one
                    i += 1
                else:
                    i += inc + total_not_needed + total_atoms
                    total_up_weight += i

        weigh(stable)
        weigh(testing)
        weigh(unstable)

        # At most one oversion of the mod must be installed
        formula.append(
            atoms[group],
            "inviolable-rule",
            "At most one version may be installed",
            atmost=1,
        )

    # Clause for each mod installed, but not selected, penalizing their removal
    # If depclean is set, we instead weigh them to remove if possible
    for mod in load_all_installed():
        if not is_selected(mod.ATOM) and Atom(mod.CPN) not in explicit:
            if depclean and deep:
                for pkg in load_pkg(Atom(mod.CPN)):
                    formula.append(
                        ["-" + pkg.ATOM],
                        weight=WEIGHTS.keep_installed + total_up_weight,
                    )
            elif update:  # If update is passed, penalize removal, but updates override
                formula.append([mod.ATOM], weight=WEIGHTS.keep_installed)
            else:  # if update is not passed, stay installed regardless of updates
                formula.append(
                    [mod.ATOM], weight=WEIGHTS.keep_installed + total_up_weight
                )
        elif Atom(mod.CPN) not in explicit and not update:
            formula.append([mod.ATOM], weight=WEIGHTS.keep_installed + total_up_weight)

    # When depcleaning, make sure the weight of installing not installed mods is higher
    # than the weight of removing unneeded mods. This prevents depcleaning from swapping out
    # mods in or expressions for each other.
    if depclean:
        for group in formula.atoms:
            for atom in formula.atoms[group]:
                if (
                    not load_installed_pkg(Atom(atom.CPN))
                    and not is_selected(atom)
                    and Atom(atom.CPN) not in explicit
                ):
                    formula.append(
                        ["-" + atom],
                        weight=WEIGHTS.not_needed
                        + total_up_weight
                        + WEIGHTS.keep_installed,
                    )
    return formula


def weigh_flags(
    flags: Iterable[FQAtom],
    explicit: AbstractSet[Atom],
    *,
    newuse: bool,
):
    formula = Formula()

    def iterate_flags():
        for flagatom in flags:
            flag = list(flagatom.USE)[0]  # Note: each only has one flag
            disabledflag = "-" + flag
            enabledatom = flagatom.lstrip("-")
            disabledatom = "-" + enabledatom
            atom_nouse = flagatom.strip_use()
            pkg = load_pkg_fq(atom_nouse)
            yield flag, disabledflag, atom_nouse, enabledatom, disabledatom, pkg

    default_weight = WEIGHTS.default_flag
    total_flag_weight = 0
    total_user_weight = 0
    # Clauses for default use flag values, with a small penalty for changes from
    #    the default setting,
    for flag, disabledflag, atom, enabledatom, disabledatom, mod in iterate_flags():
        if newuse or atom.CPN in explicit or not load_installed_pkg(mod.CPN):
            user_flags = get_user_use(mod.ATOM)
            global_user_flags = get_user_global_use()
            if flag in user_flags:
                pass
            elif disabledflag in user_flags:
                pass
            elif flag in global_user_flags:
                pass
            elif disabledflag in global_user_flags:
                pass
            elif flag in get_use(mod)[0]:  # default value
                formula.append(["-" + atom, enabledatom], weight=default_weight)
                total_flag_weight += default_weight
            else:
                formula.append(["-" + atom, disabledatom], weight=default_weight)
                total_flag_weight += default_weight
        else:
            # If not running in deep mode, keep flags the same for
            # non-selected but previously installed mods, if possible
            enabled = mod.get_enabled_use()

            if flag in enabled:
                formula.append(["-" + atom, enabledatom], weight=default_weight)
            else:
                formula.append(["-" + atom, disabledatom], weight=default_weight)

    user_weight = WEIGHTS.user_flag + total_flag_weight
    # Clauses for user flags. These will always override changes from the default value.
    for flag, disabledflag, atom, enabledatom, disabledatom, mod in iterate_flags():
        if newuse or atom.CPN in explicit or not load_installed_pkg(mod.CPN):
            user_flags = get_user_use(mod.ATOM)
            global_user_flags = get_user_global_use()
            if flag in user_flags:
                formula.append(["-" + atom, enabledatom], weight=user_weight)
                total_user_weight += user_weight
            elif disabledflag in user_flags:
                formula.append(["-" + atom, disabledatom], weight=user_weight)
                total_user_weight += user_weight
            elif flag in global_user_flags:
                formula.append(["-" + atom, enabledatom], weight=user_weight)
                total_user_weight += user_weight
            elif disabledflag in global_user_flags:
                formula.append(["-" + atom, disabledatom], weight=user_weight)
                total_user_weight += user_weight

    return formula, total_user_weight
