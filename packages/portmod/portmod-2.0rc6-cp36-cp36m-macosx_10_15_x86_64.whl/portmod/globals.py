# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import pickle
import tempfile
from functools import lru_cache
from typing import List, Optional

from appdirs import AppDirs

from .l10n import l10n


@lru_cache()
def get_version() -> str:
    """Returns portmod version"""
    try:
        from ._version import version

        return str(version)
    except ImportError:
        osp = os.path
        possible_root = osp.dirname(osp.dirname(osp.realpath(__file__)))
        if osp.isfile(osp.join(possible_root, ".portmod_not_installed")):
            # Only a dev dependency and is otherwise unneeded at runtime
            import setuptools_scm

            return str(setuptools_scm.get_version(possible_root))
        else:
            try:
                from importlib.metadata import version as version_func
            except ModuleNotFoundError:
                from importlib_metadata import version as version_func  # type: ignore

            return str(version_func("portmod"))


_DIRS = AppDirs("portmod")


class Env:
    ALLOW_LOAD_ERROR = True
    DEBUG = False
    TMP_DIR = os.path.join(tempfile.gettempdir(), "portmod")
    PYBUILD_TMP_DIR = os.path.join(TMP_DIR, "pybuild")
    WARNINGS_DIR = os.path.join(PYBUILD_TMP_DIR, "messages")
    MESSAGES_DIR = os.path.join(PYBUILD_TMP_DIR, "warnings")
    DATA_DIR = _DIRS.user_data_dir
    CONFIG_DIR = _DIRS.user_config_dir
    CACHE_DIR = _DIRS.user_cache_dir
    INTERACTIVE = True
    TESTING = False
    # Flag set when execution is ocurring within a sandboxed process
    # Certain functions will fail to execute in the sandbox (e.g. loading uncached
    # pybuilds), so this can be used to skip them.
    SANDBOX = False
    PREFIX_NAME: Optional[str] = None
    PREFIX_ARCH: Optional[str] = None
    REPOS: List["portmod.repo.Repo"]

    # The following variables are none if a prefix has not been selected
    class Prefix:
        REPOS: List["portmod.repo.Repo"]

        def __init__(self, prefix: str):
            from portmod.prefix import get_prefixes

            if prefix not in get_prefixes():
                raise Exception(l10n("invalid-prefix", prefix=prefix))

            self.ARCH = get_prefixes()[prefix]
            self.PORTMOD_CONFIG_DIR = os.path.join(env.CONFIG_DIR, prefix)
            self.SET_DIR = os.path.join(self.PORTMOD_CONFIG_DIR, "sets")
            self.PORTMOD_CONFIG = os.path.join(self.PORTMOD_CONFIG_DIR, "portmod.conf")

            self.PORTMOD_LOCAL_DIR = os.path.join(env.DATA_DIR, prefix)
            self.PACKAGE_DIR = os.path.join(self.PORTMOD_LOCAL_DIR, "pkg")
            self.INSTALLED_DB = os.path.join(self.PORTMOD_LOCAL_DIR, "db")
            self.NEWS_DIR = os.path.join(self.PORTMOD_LOCAL_DIR, "news")

            self.CACHE_DIR = os.path.join(env.CACHE_DIR, "prefix", prefix)
            self.PYBUILD_INSTALLED_CACHE = os.path.join(self.CACHE_DIR, "pybuild")
            self.CONFIG_PROTECT_DIR = os.path.join(self.CACHE_DIR, "cfg_protect")
            self.REPOS = []

    def prefix(self) -> Prefix:
        if self.PREFIX_NAME is not None:
            return self._prefix
        raise Exception("Internal error: Prefix has not been initialized!")

    def set_prefix(self, prefix: Optional[str]):
        from portmod.lock import has_prefix_exclusive_lock, has_prefix_lock
        from portmod.repos import get_repos

        if self.PREFIX_NAME:
            if has_prefix_exclusive_lock() or has_prefix_lock():
                raise Exception("Cannot change prefix while a lock is acquired!")

        if prefix:
            self._prefix = Env.Prefix(prefix)
            self.PREFIX_NAME = prefix
            self._prefix.REPOS = get_repos()
        else:
            self.PREFIX_NAME = None

    def __init__(self):
        self.PREFIX_FILE = os.path.join(self.DATA_DIR, "prefix")
        self.REPOS_DIR = os.path.join(self.DATA_DIR, "repos")
        self.PYBUILD_CACHE_DIR = os.path.join(self.CACHE_DIR, "pybuild")
        self.DOWNLOAD_DIR = os.path.join(self.CACHE_DIR, "downloads")
        self.GLOBAL_PORTMOD_CONFIG = os.path.join(self.CONFIG_DIR, "portmod.conf")
        self.REPOS_FILE = os.path.join(self.CONFIG_DIR, "repos.cfg")
        self.REPOS = []

    def serialize(self):
        result = {}
        for key in dir(self):
            if not key.startswith("__") and not callable(getattr(self, key)):
                result[key] = getattr(self, key)
        return pickle.dumps(result)

    def deserialize(self, dump: bytes):
        result = pickle.loads(dump)
        for key in result:
            setattr(self, key, result[key])


env = Env()

# Inititialize env.REPOS
import portmod.repos  # noqa isort:skip
