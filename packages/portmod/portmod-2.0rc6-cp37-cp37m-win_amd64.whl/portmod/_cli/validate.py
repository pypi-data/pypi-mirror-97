# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
from logging import error

from portmod.atom import Atom
from portmod.globals import env
from portmod.l10n import l10n
from portmod.loader import load_installed_pkg


def get_packages(path: str):
    for category in os.listdir(path):
        if os.path.isdir(os.path.join(path, category)) and not category.startswith("."):
            for package in os.listdir(os.path.join(path, category)):
                if os.path.isdir(os.path.join(path, category, package)):
                    yield category, package


def validate(args):
    # Check that mods in the DB correspond to mods in the mods directory
    for category, package in get_packages(env.prefix().INSTALLED_DB):
        # Check that mod is installed
        if not os.path.exists(
            os.path.join(env.prefix().PACKAGE_DIR, category, package)
        ):
            error(l10n("in-database-not-installed", atom=f"{category}/{package}"))

        # Check that pybuild can be loaded
        if not load_installed_pkg(Atom(f"{category}/{package}")):
            error(
                l10n(
                    "in-database-could-not-load",
                    atom=Atom(f"{category}/{package}"),
                )
            )

    # Check that all mods in the mod directory are also in the DB
    for category, package in get_packages(env.prefix().PACKAGE_DIR):
        if not os.path.exists(
            os.path.join(env.prefix().INSTALLED_DB, category, package)
        ):
            error(l10n("installed-not-in-database", atom=f"{category}/{package}"))
