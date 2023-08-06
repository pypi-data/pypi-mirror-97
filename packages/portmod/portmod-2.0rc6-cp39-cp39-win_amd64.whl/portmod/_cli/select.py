# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
CLI to select various configuration options

Currently just profiles
"""

import os
from logging import info
from typing import List

from portmod.colour import bright, green, lblue
from portmod.config import get_config, set_config_value
from portmod.globals import env
from portmod.l10n import l10n
from portmod.modules import add_parsers
from portmod.news import add_news_parsers
from portmod.repo import RemoteRepo, has_repo
from portmod.repo.metadata import get_profiles
from portmod.repos import add_repo, get_repos, parse_remote_repos
from portmod.sync import sync

from .error import InputException


def display_list(items, notes, selected):
    padding = len(str(len(items)))
    for index, (item, note) in enumerate(zip(items, notes)):
        selected_str = ""
        if index in selected:
            selected_str = lblue("*")
        index_str = bright("[" + str(index) + "]")
        print(
            f'  {index_str} {" " * (padding - len(str(index))) + item} ({note})',
            selected_str,
        )


def add_profile_parsers(subparsers, parents):
    profile = subparsers.add_parser(
        "profile", help=l10n("profile-help"), parents=parents
    )
    profile_subparsers = profile.add_subparsers()
    profile_list = profile_subparsers.add_parser("list", help=l10n("profile-list-help"))
    profile_set = profile_subparsers.add_parser("set", help=l10n("profile-set-help"))
    profile_set.add_argument(
        "index", metavar=l10n("number-placeholder"), help=l10n("profile-number-help")
    )
    profile_show = profile_subparsers.add_parser("show", help=l10n("profile-show-help"))

    def get_profile():
        linkpath = os.path.join(env.prefix().PORTMOD_CONFIG_DIR, "profile")
        if os.path.exists(linkpath) and os.path.islink(linkpath):
            return os.readlink(linkpath).split("profiles")[-1].lstrip(os.path.sep)
        return None

    def list_func(args):
        profiles = get_profiles()
        print(bright(green(l10n("profile-available"))))
        display_list(
            [profile for _, profile, _ in profiles],
            [stability for _, _, stability in profiles],
            [
                index
                for index, (_, profile, _) in enumerate(profiles)
                if profile == get_profile()
            ],
        )

    def set_func(args):
        os.makedirs(env.prefix().PORTMOD_CONFIG_DIR, exist_ok=True)
        linkpath = os.path.join(env.prefix().PORTMOD_CONFIG_DIR, "profile")
        if os.path.exists(linkpath):
            os.unlink(linkpath)
        (path, _, _) = get_profiles()[int(args.index)]
        os.symlink(path, linkpath)

    def show_func(args):
        linkpath = os.path.join(env.prefix().PORTMOD_CONFIG_DIR, "profile")
        print(bright(green(l10n("profile-current-symlink", path=linkpath))))
        print(
            "  "
            + bright(os.readlink(linkpath).split("profiles")[-1].lstrip(os.path.sep))
        )

    def profile_help(args):
        profile.print_help()

    profile.set_defaults(func=profile_help)
    profile_list.set_defaults(func=list_func)
    profile_set.set_defaults(func=set_func)
    profile_show.set_defaults(func=show_func)


def add_repo_parser(subparsers, parents):
    repo = subparsers.add_parser("repo", help=l10n("repo-help"), parents=parents)
    repo_subparsers = repo.add_subparsers()
    repo_list = repo_subparsers.add_parser("list", help=l10n("repo-list-help"))
    repo_add = repo_subparsers.add_parser("add", help=l10n("repo-add-help"))
    repo_add.add_argument(
        "repo", metavar=l10n("repo-placeholder"), help=l10n("repo-identifier-help")
    )
    repo_remove = repo_subparsers.add_parser("remove", help=l10n("repo-remove-help"))
    repo_remove.add_argument(
        "repo", metavar=l10n("repo-placeholder"), help=l10n("repo-identifier-help")
    )

    def get_repos_list() -> List[RemoteRepo]:
        repos = []
        for repo in env.REPOS:
            conf = os.path.join(repo.location, "metadata", "repos.cfg")
            if os.path.exists(conf):
                repos.extend(parse_remote_repos(conf))
        return repos

    def list_func(args):
        repos = get_repos_list()
        print(bright(green(l10n("repos-available"))))
        display_list(
            [bright(repo.name) + ": " + repo.description for repo in repos],
            [repo.quality + " " + lblue(repo.sync_uri) for repo in repos],
            [index for index, repo in enumerate(repos) if has_repo(repo.name)],
        )

    def get_repo_name(value: str) -> str:
        repos = get_repos_list()
        if value.isdigit():
            repo_name = repos[int(value)].name
        else:
            if any(repo.name == value for repo in repos):
                repo_name = value
            else:
                raise InputException(l10n("repo-does-not-exist", name=value))

        return repo_name

    def add_func(args):
        enabled_repos = get_config()["REPOS"]
        repo_name = get_repo_name(args.repo)

        if repo_name and repo_name not in enabled_repos:
            enabled_repos.add(repo_name)
            info(l10n("repo-adding", name=repo_name, conf=env.prefix().PORTMOD_CONFIG))

        set_config_value("REPOS", " ".join(sorted(enabled_repos)))

        repo = next(repo for repo in get_repos_list() if repo.name == repo_name)
        result = add_repo(repo)
        if result:
            sync([result])
        env.REPOS = get_repos()

    def remove_func(args):
        enabled_repos = get_config()["REPOS"]
        repo_name = get_repo_name(args.repo)

        if repo_name and repo_name in enabled_repos:
            enabled_repos.remove(repo_name)
            info(
                l10n("repo-removing", name=repo_name, conf=env.prefix().PORTMOD_CONFIG)
            )

        set_config_value("REPOS", " ".join(sorted(enabled_repos)))

    def repo_help(args):
        repo.print_help()

    repo.set_defaults(func=repo_help)
    repo_list.set_defaults(func=list_func)
    repo_add.set_defaults(func=add_func)
    repo_remove.set_defaults(func=remove_func)


def add_select_parser(subparsers, parents):
    """
    Adds the select subparser to the given subparsers
    """
    parser = subparsers.add_parser("select", help=l10n("select-help"), parents=parents)
    _subparsers = parser.add_subparsers()
    add_profile_parsers(_subparsers, parents)
    add_news_parsers(_subparsers, parents)
    add_repo_parser(_subparsers, parents)
    add_parsers(_subparsers, parents)
    parser.set_defaults(func=lambda args: parser.print_help())
