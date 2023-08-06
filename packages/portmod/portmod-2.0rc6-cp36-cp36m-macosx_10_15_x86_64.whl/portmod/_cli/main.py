# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import argparse
import os
import sys
import traceback
from logging import error
from typing import Optional, cast

from portmod.atom import Atom
from portmod.config import config_to_string, get_config
from portmod.config.sets import get_system
from portmod.globals import env, get_version
from portmod.l10n import l10n
from portmod.loader import load_installed_pkg
from portmod.log import add_logging_arguments, init_logger
from portmod.modules import handle_cfg_protect
from portmod.prefix import get_prefixes
from portmod.repos import get_local_repos
from portmod.sync import sync
from portmod.transactions import get_usestrings

from .conflicts import add_conflicts_parser
from .error import InputException
from .init import add_init_parser
from .merge import add_merge_parser
from .mirror import add_mirror_parser
from .query import add_query_parser
from .search import add_search_parser
from .select import add_select_parser
from .use import add_use_parser
from .validate import validate


def add_info_parser(subparsers, parents):
    def info(args):
        from git import Repo

        print(f"Portmod {get_version()}")
        print(f"Python {sys.version}")
        print()

        print(l10n("info-repositories"))
        for repo in env.prefix().REPOS:
            gitrepo = Repo.init(repo.location)
            print("    ", "\n         ".join(str(repo).split(",")))
            print(
                "    ",
                l10n(
                    "info-repository-date", date=gitrepo.head.commit.committed_datetime
                ),
            )
            print("    ", l10n("info-repository-commit", commit=gitrepo.head.commit))
            print()

        generator = (
            load_installed_pkg(atom)
            for atom in get_system() | set(map(Atom, get_config()["INFO_PACKAGES"]))
            if load_installed_pkg(atom)
        )
        packages = set(filter(None, generator))
        length = max(len(x.CPN) for x in packages)
        for pkg in sorted(packages, key=lambda x: x.CPN):
            # FIXME: Display date package was installed for live packages
            usestrings = filter(None, get_usestrings(pkg, pkg.INSTALLED_USE, True))
            padding = length - len(str(pkg.CPN))
            print(pkg.CPN + ":", " " * padding, pkg.PVR, *usestrings)
        print()

        # Print config values
        config = get_config()
        if args.verbose:
            print(config_to_string(config))
        else:
            print(
                config_to_string(
                    {
                        entry: config[entry]
                        for entry in config
                        if entry in config["INFO_VARS"]
                    }
                )
            )
        # Print hardcoded portmod paths
        print(f"TMP_DIR = {env.TMP_DIR}")
        print(f"CACHE_DIR = {env.CACHE_DIR}")
        print(f"PORTMOD_CONFIG_DIR = {env.prefix().PORTMOD_CONFIG_DIR}")
        print(f"PORTMOD_LOCAL_DIR = {env.prefix().PORTMOD_LOCAL_DIR}")
        sys.exit(0)

    parser = subparsers.add_parser("info", help=l10n("info-help"), parents=parents)
    parser.set_defaults(func=info)


def parse_args(
    subcommand: Optional[str] = None, prefix_subcommand: Optional[str] = None
):
    common = argparse.ArgumentParser(add_help=False)
    add_logging_arguments(common)
    common.add_argument("--debug", help=l10n("merge-debug-help"), action="store_true")

    parser = argparse.ArgumentParser(description=l10n("description"), parents=[common])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--version", help=l10n("version-help"), action="store_true")

    subparsers = parser.add_subparsers(dest="subcommand_name")

    if subcommand is None or subcommand in get_prefixes() and prefix_subcommand is None:
        prefix_parsers_list = []

        def get_help_func(parser):
            func = parser.print_help
            return lambda args: func()

        for prefix in get_prefixes():
            prefix_parser = subparsers.add_parser(
                prefix, help=l10n("prefix-help", prefix=prefix), parents=[common]
            )
            prefix_parsers_list.append(
                prefix_parser.add_subparsers(dest="prefix_subcommand_name")
            )
            prefix_parser.set_defaults(func=get_help_func(prefix_parser))

        for subparser in prefix_parsers_list:
            subparser.add_parser("merge", help=l10n("merge-help"), add_help=False)
            subparser.add_parser("search", help=l10n("search-help"), add_help=False)
            subparser.add_parser("select", help=l10n("select-help"), add_help=False)
            subparser.add_parser("query", help=l10n("query-help"), add_help=False)
            subparser.add_parser("use", help=l10n("use-help"), add_help=False)
            subparser.add_parser(
                "conflict-ui", help=l10n("conflict-ui-help"), add_help=False
            )
            subparser.add_parser("info", help=l10n("info-help"), add_help=False)
            subparser.add_parser("validate", help=l10n("validate-help"), add_help=False)
        subparsers.add_parser("mirror", help=l10n("mirror-help"), add_help=False)
    elif subcommand in get_prefixes():
        prefix = subcommand

        prefix_parser = subparsers.add_parser(
            prefix, help=l10n("prefix-help", prefix=prefix), parents=[common]
        )
        prefix_parsers = prefix_parser.add_subparsers(dest="prefix_subcommand_name")
        prefix_parser.set_defaults(func=lambda args: prefix_parser.print_help())
        if prefix_subcommand == "merge":
            add_merge_parser(prefix_parsers, [common])
        elif prefix_subcommand == "search":
            add_search_parser(prefix_parsers, [common])
        elif prefix_subcommand == "select":
            add_select_parser(prefix_parsers, [common])
        elif prefix_subcommand == "query":
            add_query_parser(prefix_parsers, [common])
        elif prefix_subcommand == "use":
            add_use_parser(prefix_parsers, [common])
        elif prefix_subcommand == "conflict-ui":
            add_conflicts_parser(prefix_parsers, [common])
        elif prefix_subcommand == "info":
            add_info_parser(prefix_parsers, [common])
        elif prefix_subcommand == "validate":
            prefix_parsers.add_parser(
                "validate", help=l10n("validate-help"), parents=[common]
            ).set_defaults(func=validate)
    elif subcommand == "mirror":
        add_mirror_parser(subparsers, [common])

    add_init_parser(subparsers, parents=[common])
    subparsers.add_parser(
        "sync", help=l10n("sync-help"), parents=[common]
    ).set_defaults(func=lambda args: sync(get_local_repos().values()))

    try:
        import argcomplete  # pylint: disable=import-error

        argcomplete.autocomplete(parser)
    except ModuleNotFoundError:
        pass

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    if "--ignore-default-opts" in sys.argv:
        args = sys.argv[1:]
    else:
        args = sys.argv[1:] + os.environ.get("OMWMERGE_DEFAULT_OPTS", "").split()

    if subcommand is None:
        return parser.parse_known_args(args)[0]
    else:
        return parser.parse_args(args)


def is_old_structure() -> bool:
    """
    Determine if installation data from the alpha/beta releases
    are installed on this system
    """
    return os.path.exists(os.path.join(env.DATA_DIR, "mods"))


def migrate():
    """
    Migrates installation data from alpha/beta to new system
    """
    # TODO: Remove this migration code at before the 2.0 release
    # This is NOT a feature, but rather a temporary convenience
    # Post 2.0, users who still want to migrate installations from alpha/beta should
    # first install a release candidate to make use of the migration code,
    # then switch to the latest release
    import re
    import shutil
    from logging import warning

    from portmod.config import set_config_value
    from portmod.prefix import add_prefix
    from portmod.prompt import prompt_bool, prompt_str
    from portmod.repos import get_local_repos
    from portmod.sync import sync

    if not prompt_bool(
        """
    Old data from the alpha or beta version of portmod has been detected.
    Would you like to automatically migrate this data to the new system?
    There will not be an option later to reverse this automatically (though it is possible to do it manually)
    """
    ):
        sys.exit(1)

    prefix = prompt_str(
        """What would you like to call your new prefix?

This will be used in commands (e.g. portmod <prefix> merge) to identify the prefix.

It is also recommended that you create aliases for your prefixes, such as (in bash):
alias omwmerge="portmod openmw merge"
    """,
        "openmw",
    )

    if prefix is None:
        sys.exit(1)

    if os.path.exists(os.path.join(env.DATA_DIR, "openmw")):
        # If they use the (old) default location for the openmw repo
        # Move it into the new default location
        os.makedirs(env.REPOS_DIR, exist_ok=True)
        shutil.move(
            os.path.join(env.DATA_DIR, "openmw"), os.path.join(env.REPOS_DIR, "openmw")
        )
        # If path is in repos.cfg, rewrite it
        import configparser

        repo_config = configparser.ConfigParser(
            comment_prefixes="/", allow_no_value=True
        )
        repo_config.read(env.REPOS_FILE)
        if "openmw" in repo_config:
            repo_config.set("openmw", "location", os.path.join(env.REPOS_DIR, "openmw"))
            with open(env.REPOS_FILE, "w") as repos_file:
                repo_config.write(repos_file)

    meta_repo = get_local_repos()["meta"]
    sync([meta_repo])

    # Create and enter openmw prefix
    add_prefix(prefix, get_config().get("ARCH") or "openmw")
    env.set_prefix(prefix)

    shutil.move(os.path.join(env.DATA_DIR, "mods"), env.prefix().PACKAGE_DIR)

    # Move old data into new prefix
    data_files = set(os.listdir(env.DATA_DIR)) - {"repos", prefix, "prefix"}
    if os.path.exists(env.prefix().INSTALLED_DB):
        # db has already been initialized as part of prefix initialization
        shutil.rmtree(env.prefix().INSTALLED_DB)
    os.makedirs(env.prefix().PORTMOD_LOCAL_DIR, exist_ok=True)
    for file in data_files:
        shutil.move(
            os.path.join(env.DATA_DIR, file),
            os.path.join(env.prefix().PORTMOD_LOCAL_DIR, file),
        )

    # Move old config files into new prefix
    config_files = set(os.listdir(env.CONFIG_DIR)) - {"repos.cfg", prefix}
    os.makedirs(env.prefix().PORTMOD_CONFIG_DIR, exist_ok=True)
    for file in config_files:
        if file.startswith("mod."):
            shutil.move(
                os.path.join(env.CONFIG_DIR, file),
                os.path.join(
                    env.prefix().PORTMOD_CONFIG_DIR, re.sub(r"^mod\.", "package.", file)
                ),
            )
        else:
            shutil.move(
                os.path.join(env.CONFIG_DIR, file),
                os.path.join(env.prefix().PORTMOD_CONFIG_DIR, file),
            )

    # Delete old pybuild cache
    if os.path.exists(os.path.join(env.CACHE_DIR, "pybuild")):
        shutil.rmtree(os.path.join(env.CACHE_DIR, "pybuild"))

    # Move old cfg_protect dir into prefix
    if os.path.exists(os.path.join(env.CACHE_DIR, "cfg_protect")):
        os.makedirs(env.CACHE_DIR, exist_ok=True)
        shutil.move(
            os.path.join(env.CACHE_DIR, "cfg_protect"), env.prefix().CONFIG_PROTECT_DIR
        )

    set_config_value("REPOS", "openmw")

    warning(
        "Exiting portmod so that settings can be reloaded properly. "
        "While this could be done in-process, it's more work than it's worth\n"
        "Your previous command has not been executed. "
        "If it was important, you will need to run it again."
    )
    sys.exit(1)


def main():
    os.environ["PYTHONUNBUFFERED"] = "1"

    if is_old_structure():
        migrate()

    args = parse_args()
    init_logger(args)

    if args.subcommand_name in get_prefixes():
        env.set_prefix(args.subcommand_name)

        # Ensure that we read config entries into os.environ
        get_config()

        if os.path.exists(os.path.join(env.prefix().SET_DIR, "world")):
            from portmod.atom import Atom
            from portmod.config.sets import add_set
            from portmod.parsers.list import read_list

            # FIXME: Remove
            # Bug in 2.0_rc0 and 2.0_rc1 caused selected packages to be written to
            # the wrong file
            for atom in read_list(os.path.join(env.prefix().SET_DIR, "world")):
                add_set("selected-packages", Atom(atom))
            os.remove(os.path.join(env.prefix().SET_DIR, "world"))

    prefix_subcommand_name = None
    if hasattr(args, "prefix_subcommand_name"):
        prefix_subcommand_name = cast(str, args.prefix_subcommand_name)
    args = parse_args(args.subcommand_name, prefix_subcommand_name)

    env.DEBUG = args.debug

    init_logger(args)

    if args.version:
        print(f"Portmod {get_version()}")
        sys.exit(0)

    try:
        args.func(args)
        if args.subcommand_name in get_prefixes():
            handle_cfg_protect()
    except InputException as e:
        error("{}".format(e))
        sys.exit(1)
    except Exception as e:
        traceback.print_exc()
        error("{}".format(e))
        sys.exit(1)
