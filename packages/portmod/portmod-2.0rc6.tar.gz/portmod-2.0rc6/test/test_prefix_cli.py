# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests some otherwise untested parts of the interface
"""

import os
import sys

import pytest

from portmod._cli.main import main
from portmod.atom import Atom
from portmod.globals import env
from portmod.loader import load_installed_pkg

from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    yield setup_env("test")
    tear_down_env()


def test_validate():
    """Tests that validate works correctly"""
    sys.argv = ["portmod", "test", "merge", "test", "test2", "--no-confirm"]
    main()
    sys.argv = ["portmod", "test", "validate"]
    main()


def test_sync():
    """Tests that portmod sync works correctly"""
    sys.argv = ["portmod", "sync"]
    main()


def test_info():
    """Tests that portmod sync works correctly"""
    sys.argv = ["portmod", "test", "info"]
    with pytest.raises(SystemExit):
        main()


def test_search():
    """Tests that portmod sync works correctly"""
    sys.argv = ["portmod", "test", "search", "test"]
    main()


def test_use():
    """Tests that portmod sync works correctly"""
    sys.argv = ["portmod", "test", "use", "-E", "foo"]
    main()
    sys.argv = ["portmod", "test", "merge", "test4", "--no-confirm"]
    main()
    pkg = load_installed_pkg(Atom("test/test4"))
    assert pkg
    assert "foo" in pkg.get_enabled_use()


@pytest.mark.xfail(
    sys.platform == "win32" and "APPVEYOR" in os.environ,
    reason="For some reason the vdb git repo can't be removed during cleanup",
    raises=PermissionError,
)
def test_mirror():
    """Tests that portmod --version works correctly"""
    sys.argv = ["portmod", "mirror", os.path.join(env.TMP_DIR, "mirror")]
    main()
