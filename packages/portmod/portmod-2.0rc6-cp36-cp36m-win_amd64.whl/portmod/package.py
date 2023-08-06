# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import json
import lzma
import os
import shutil
from logging import error, info, warning
from typing import Dict, List, Optional, Set, cast

from portmod.atom import Atom
from portmod.colour import green
from portmod.download import download_mod
from portmod.globals import env
from portmod.loader import (
    _delete_state,
    _sandbox_execute_pybuild,
    _state_path,
    load_installed_pkg,
)
from portmod.lock import vdb_lock

from .cache import clear_cache_for_path
from .fs.util import get_tree_size, onerror
from .functools import clear_install_cache
from .l10n import l10n
from .parsers.manifest import Manifest
from .perms import Permissions
from .pybuild import InstalledPybuild, Pybuild, Source
from .rebuild import get_rebuild_manifest
from .vfs import _cleanup_tmp_archive_dir


class PhaseState:
    """
    Information passed to the phase functions for use during execution

    These fields match those of the same names listed and documented
    by :class:`~pybuild.Pybuild1`
    """

    A: List[Source]
    FILESDIR: str
    T: Optional[str]
    D: str
    USE: Set[str]
    WORKDIR: str
    ROOT: str
    UNFETCHED: List[Source]
    S: Optional[str]

    def __init__(self, build_dir: Optional[str] = None):
        if build_dir:
            self.T = os.path.join(build_dir, "temp")
        else:
            self.T = None

    @classmethod
    def from_json(cls, dictionary: Dict):
        new = PhaseState()
        for key, value in dictionary.items():
            setattr(new, key, value)
        if hasattr(new, "A"):
            new.A = [Source(**x) for x in cast(Dict, new.A)]
        if hasattr(new, "UNFETCHED"):
            new.UNFETCHED = [Source(**x) for x in cast(Dict, new.UNFETCHED)]
        return new


def get_pkg_path(mod: Pybuild) -> str:
    return os.path.join(env.prefix().PACKAGE_DIR, mod.CATEGORY, mod.PN)


def src_unpack(
    pkg: Pybuild,
    build_dir: str,
    curdir: Optional[str] = None,
    state: PhaseState = PhaseState(),
):
    permissions = Permissions(
        rw_paths=[build_dir],
        ro_paths=[env.DOWNLOAD_DIR],
        global_read=False,
        network=True,
        tmp=state.T,
    )
    _sandbox_execute_pybuild(
        pkg.FILE,
        "unpack",
        permissions,
        save_state=True,
        init=state.__dict__,
        curdir=curdir or build_dir,
    )


def src_prepare(
    pkg: Pybuild,
    build_dir: str,
    curdir: Optional[str] = None,
    state: PhaseState = PhaseState(),
):
    # Default does nothing unless pkg.PATCHES is set
    if pkg.PATCHES or "src_prepare" in pkg.FUNCTIONS:
        permissions = Permissions(
            rw_paths=[build_dir], global_read=True, network=False, tmp=state.T
        )
        _sandbox_execute_pybuild(
            pkg.FILE,
            "prepare",
            permissions,
            save_state=True,
            init=state.__dict__,
            curdir=curdir or build_dir,
        )


def src_install(
    pkg: Pybuild,
    build_dir: str,
    curdir: Optional[str] = None,
    state: PhaseState = PhaseState(),
):
    permissions = Permissions(
        rw_paths=[build_dir], global_read=True, network=False, tmp=state.T
    )
    _sandbox_execute_pybuild(
        pkg.FILE,
        "install",
        permissions,
        save_state=True,
        init=state.__dict__,
        curdir=curdir or build_dir,
    )


def pkg_postinst(
    pkg: Pybuild, final_install: str, curdir: str, state: PhaseState = PhaseState()
):
    # Default does nothing
    if "pkg_postinst" in pkg.FUNCTIONS:
        permissions = Permissions(
            rw_paths=[final_install],
            global_read=True,
            network=False,
            tmp=state.T,
        )
        _sandbox_execute_pybuild(
            pkg.FILE,
            "postinst",
            permissions,
            save_state=True,
            init=state.__dict__,
            curdir=curdir,
        )


def pkg_prerm(pkg: Pybuild, root: str, state: PhaseState = PhaseState()):
    # Default does nothing
    if "pkg_prerm" in pkg.FUNCTIONS:
        permissions = Permissions(
            rw_paths=[root], global_read=True, network=False, tmp=state.T
        )
        _sandbox_execute_pybuild(
            pkg.FILE,
            "prerm",
            permissions,
            save_state=False,
            init=state.__dict__,
            curdir=root,
        )
    if "module" in pkg.PROPERTIES:
        from .modules import iterate_pkg_modules

        for module in iterate_pkg_modules(pkg):
            module.prerm()


def remove_pkg(mod: InstalledPybuild, reinstall: bool = False):
    """
    Removes the given mod

    args:
        reinstall: if true, don't touch the installed DB since we'll
                   need it to finish the install
    """
    # Slow imports
    import git

    print(">>> " + l10n("pkg-removing", atom=green(mod.ATOM.CPF)))

    path = get_pkg_path(mod)

    BUILD_DIR = os.path.join(env.TMP_DIR, mod.CATEGORY, mod.P)
    state = PhaseState(BUILD_DIR)
    assert state.T

    state.USE = mod.INSTALLED_USE
    os.makedirs(state.T, exist_ok=True)

    if os.path.exists(path):
        state.ROOT = path
        pkg_prerm(mod, path, state)
        del state.ROOT

        if os.path.islink(path):
            os.remove(path)
        else:
            shutil.rmtree(path, onerror=onerror)

    db_path = os.path.join(env.prefix().INSTALLED_DB, mod.CATEGORY, mod.PN)
    if os.path.exists(db_path) and not reinstall:
        # Remove and stage changes
        gitrepo = git.Repo.init(env.prefix().INSTALLED_DB)
        gitrepo.git.rm(os.path.join(mod.CATEGORY, mod.PN), r=True, f=True)
        # Clean up unstaged files (e.g. pycache)
        with vdb_lock(write=True):
            shutil.rmtree(db_path, ignore_errors=True, onerror=onerror)
            clear_cache_for_path(os.path.join(db_path, os.path.basename(mod.FILE)))

    # Remove from pybuild cache
    path = os.path.join(env.prefix().PYBUILD_INSTALLED_CACHE, mod.CATEGORY, mod.PF)
    if os.path.exists(path):
        os.remove(path)

    # Cleanup archive dir in case vfs had to extract anything
    _cleanup_tmp_archive_dir()

    print(">>> " + l10n("pkg-finished-removing", atom=green(mod.ATOM.CPF)))
    clear_install_cache()


def install_pkg(mod: Pybuild):
    # Slow imports
    import git

    print(">>> " + l10n("pkg-installing", atom=green(mod.ATOM.CPF)))
    old_curdir = os.getcwd()
    sources = download_mod(mod)
    if sources is None:
        error(">>> " + l10n("pkg-unable-to-download", atom=green(mod.ATOM.CPF)))
        return False

    BUILD_DIR = os.path.join(env.TMP_DIR, mod.CATEGORY, mod.P)
    state = PhaseState(BUILD_DIR)
    assert state.T
    state.A = [source.as_source() for source in sources]
    state.USE = mod.get_use()[0]

    # Ensure build directory is clean
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR, onerror=onerror)

    state.WORKDIR = os.path.join(BUILD_DIR, "work")
    # copy files from filesdir into BUILD_DIR/files so that they are accessible
    # from within the sandbox
    FILESDIR = os.path.join(os.path.dirname(mod.FILE), "files")
    state.FILESDIR = os.path.join(BUILD_DIR, "files")
    if os.path.exists(FILESDIR):
        shutil.copytree(FILESDIR, state.FILESDIR)
    os.makedirs(state.WORKDIR, exist_ok=True)
    os.makedirs(state.T, exist_ok=True)

    info(">>> " + l10n("pkg-unpacking"))
    # Network access is allowed exclusively during src_unpack, and
    # adds additional filesystem restrictions to the sandbox
    src_unpack(mod, BUILD_DIR, state.WORKDIR, state)

    if not mod.S:
        state.S = mod.S = mod.get_default_source_basename()

    if mod.S and os.path.exists(os.path.join(state.WORKDIR, mod.S)):
        WORKDIR = os.path.join(state.WORKDIR, mod.S)
    else:
        WORKDIR = state.WORKDIR

    info(">>> " + l10n("pkg-preparing", dir=WORKDIR))

    src_prepare(mod, BUILD_DIR, WORKDIR, state)

    info(">>> " + l10n("pkg-prepared"))

    final_install_dir = os.path.join(env.prefix().PACKAGE_DIR, mod.CATEGORY)
    os.makedirs(final_install_dir, exist_ok=True)
    final_install = os.path.join(final_install_dir, mod.PN)

    state.D = os.path.join(BUILD_DIR, "image")
    os.makedirs(state.D, exist_ok=True)
    info(">>> " + l10n("pkg-installing-into", dir=state.D, atom=green(mod.ATOM.CPF)))
    src_install(mod, BUILD_DIR, WORKDIR, state)
    info(">>> " + l10n("pkg-installed-into", dir=state.D, atom=green(mod.ATOM.CPF)))

    os.chdir(env.TMP_DIR)

    if os.path.islink(state.D):
        installed_size = 0.0
    else:
        installed_size = get_tree_size(state.D) / 1024 / 1024

    build_size = get_tree_size(WORKDIR) / 1024 / 1024

    info("")
    info(f' {green("*")} ' + l10n("pkg-final-size-build", size=build_size))
    info(f' {green("*")} ' + l10n("pkg-final-size-installed", size=installed_size))
    info("")

    # If a previous version of this mod was already installed,
    # remove it before doing the final copy
    old_mod = load_installed_pkg(Atom(mod.CPN))
    db_path = os.path.join(env.prefix().INSTALLED_DB, mod.CATEGORY, mod.PN)
    if old_mod:
        remove_pkg(old_mod, os.path.exists(db_path) and mod.INSTALLED)

    info(
        ">>> "
        + l10n("pkg-installing-into", dir=final_install, atom=green(mod.ATOM.CPF))
    )

    if os.path.islink(final_install):
        os.remove(final_install)

    if os.path.exists(final_install):
        warning(l10n("pkg-existing-install-dir"))
        shutil.rmtree(final_install, onerror=onerror)

    # base/morrowind links the D directory to the morrowind install.
    # Copy the link, not the morrowind install
    if os.path.islink(state.D):
        linkto = os.readlink(state.D)
        os.symlink(linkto, final_install)
    else:
        shutil.copytree(state.D, final_install)

    state.ROOT = final_install
    pkg_postinst(mod, final_install, state.ROOT, state)

    # If installed database exists and there is no old mod, remove it
    if os.path.exists(db_path) and not old_mod:
        shutil.rmtree(db_path, onerror=onerror)

    with vdb_lock(write=True):
        # Update db entry for installed mod
        gitrepo = git.Repo.init(env.prefix().INSTALLED_DB)
        os.makedirs(db_path, exist_ok=True)

        # Copy pybuild to DB
        # unless source pybuild is in DB (i.e we're reinstalling)
        if not mod.FILE.startswith(db_path):
            shutil.copy(mod.FILE, db_path)
        gitrepo.git.add(os.path.join(mod.CATEGORY, mod.PN, os.path.basename(mod.FILE)))

        manifest_path = os.path.join(os.path.dirname(mod.FILE), "Manifest")
        if os.path.exists(manifest_path):
            # Copy Manifest to DB
            if not mod.FILE.startswith(db_path):
                shutil.copy(manifest_path, db_path)
            gitrepo.git.add(os.path.join(mod.CATEGORY, mod.PN, "Manifest"))

        def add_installed(field: str, value: str):
            with open(os.path.join(db_path, field), "w") as use:
                print(value, file=use)
            gitrepo.git.add(os.path.join(mod.CATEGORY, mod.PN, field))

        # Copy installed use configuration to DB
        add_installed("USE", " ".join(mod.get_use()[0]))
        # Copy repo pybuild was from to DB
        add_installed("REPO", mod.REPO)

        def fix_common(depstring: str):
            """
            Adds operator to dependencies in the common category
            to ensure this package is rebuilt if they change.
            """
            deps = depstring.split()
            for index, dep in enumerate(deps):
                if dep.startswith("common/"):
                    pkg = load_installed_pkg(Atom(dep))
                    # Note tilde operator. Revision bumps to
                    # common packages won't cause rebuilds.
                    if pkg:
                        deps[index] = f"~{dep}-{pkg.PV}"
            return " ".join(deps)

        # Store installed dependencies
        add_installed("RDEPEND", fix_common(mod.RDEPEND))

        # Copy pybuild environment to DB
        shutil.copy(
            os.path.join(_state_path(mod.FILE), "environment.xz"),
            os.path.join(db_path, "environment.xz"),
        )
        _delete_state(mod.FILE)
        gitrepo.git.add(os.path.join(mod.CATEGORY, mod.PN, "environment.xz"))

        path = os.path.join(db_path, "environment.xz")
        if os.path.exists(path):
            compressed_environment = lzma.LZMAFile(path)
            try:
                environment = json.load(compressed_environment)
            except EOFError as e:
                raise RuntimeError(f"Failed to read {path}") from e

            if "REBUILD_FILES" in environment and environment["REBUILD_FILES"]:
                manifest = Manifest()
                for entry in get_rebuild_manifest(environment["REBUILD_FILES"]):
                    manifest.add_entry(entry)
                manifest.write(os.path.join(db_path, "REBUILD_FILES"))

        clear_cache_for_path(os.path.join(db_path, os.path.basename(mod.FILE)))

        os.chdir(old_curdir)
        print(">>> " + l10n("pkg-installed", atom=green(mod.ATOM.CPF)))
        info("")

        if not env.DEBUG:
            shutil.rmtree(BUILD_DIR, onerror=onerror)
            # Cleanup archive dir in case vfs had to extract anything
            _cleanup_tmp_archive_dir()
            info(">>> " + l10n("cleaned-up", dir=BUILD_DIR))

        clear_install_cache()
        return True
