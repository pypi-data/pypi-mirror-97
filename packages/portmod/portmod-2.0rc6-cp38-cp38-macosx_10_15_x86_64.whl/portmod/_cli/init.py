# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3


import os

from portmod.l10n import l10n
from portmod.prefix import add_prefix
from portmod.repo import get_repo
from portmod.repo.metadata import get_archs
from portmod.sync import sync


def init(args):
    """Initializes a prefix"""
    add_prefix(args.prefix, args.arch)


def add_init_parser(subparsers, parents):
    parser = subparsers.add_parser("init", help=l10n("init-help"), parents=parents)
    parser.add_argument(
        "prefix", metavar=l10n("prefix-placeholder"), help=l10n("init-prefix-help")
    )
    try:
        meta_repo = get_repo("meta")
        if not os.path.exists(meta_repo.location):
            sync([meta_repo])
        parser.add_argument(
            "arch", help=l10n("init-arch-help"), choices=get_archs(meta_repo.location)
        )
    except Exception:
        parser.add_argument("arch", help=l10n("init-arch-help"))
    parser.set_defaults(func=init)
