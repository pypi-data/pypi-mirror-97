# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import sys

import pytest

from portmod.atom import Atom, version_gt
from portmod._deps import resolve
from portmod.merge import configure
from portmod.transactions import Downgrade, New, Reinstall, Update

from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_simple(setup):
    """Tests that simple dependency resolution works"""
    selected = {Atom("test/test")}
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert transactions.pkgs[0].pkg.CPN == "test/test"
    assert isinstance(transactions.pkgs[0], New)

    configure(["test/test"], no_confirm=True)
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert transactions.pkgs[0].pkg.CPN == "test/test"
    assert isinstance(transactions.pkgs[0], Reinstall)


def test_rebuild(setup):
    """
    Tests that packages are selected to be rebuilt, even if we don't
    use the Category-PackageName format
    """
    selected = {Atom("~test/test-1.0")}
    configure(selected, no_confirm=True)
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert transactions.pkgs[0].pkg.CPN == "test/test"
    assert transactions.pkgs[0].pkg.REPO == "test"
    assert isinstance(transactions.pkgs[0], Reinstall)


def test_upgrade(setup):
    """Tests that upgrades resolve correctly"""
    selected = {Atom("test/test")}
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert version_gt(transactions.pkgs[0].pkg.PVR, "1.0")
    assert isinstance(transactions.pkgs[0], Update)


def test_oneshot(setup):
    """Tests that oneshot resolves correctly"""
    selected = {Atom("test/test")}
    configure(selected, no_confirm=True)
    transactions = resolve(selected, set(), selected, set(), set())
    assert len(transactions.pkgs) == 1
    assert not version_gt(transactions.pkgs[0].pkg.PVR, "2.0")
    assert not version_gt("2.0", transactions.pkgs[0].pkg.PVR)
    assert isinstance(transactions.pkgs[0], Reinstall)
    assert not transactions.new_selected


@pytest.mark.xfail(
    sys.platform == "win32" and "APPVEYOR" in os.environ,
    reason="For some reason a file is being accessed by another process",
    raises=PermissionError,
)
def test_downgrade(setup):
    """Tests that downgrades resolve correctly"""
    configure(["=test/test-2.0"], no_confirm=True)
    selected = {Atom("=test/test-1.0")}
    transactions = resolve(selected, set(), selected, selected, set())
    assert len(transactions.pkgs) == 1
    assert version_gt("2.0", transactions.pkgs[0].pkg.PVR)
    assert isinstance(transactions.pkgs[0], Downgrade)
