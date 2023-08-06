# Portmod
[![pipeline](https://gitlab.com/portmod/portmod/badges/master/pipeline.svg)](https://gitlab.com/portmod/portmod/-/commits/master)
[![Build status](https://ci.appveyor.com/api/projects/status/73nlk92oj22jbyfj/branch/master?svg=true&passingText=Windows%20OK&failingText=windows%20failed)](https://ci.appveyor.com/project/portmod/portmod/branch/master)
[![coverage](https://gitlab.com/portmod/portmod/badges/master/coverage.svg)](https://gitlab.com/portmod/portmod/-/commits/master)
[![PyPI](https://img.shields.io/pypi/v/portmod)](https://pypi.org/project/portmod/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Supported Python
versions](https://img.shields.io/pypi/pyversions/portmod.svg)](https://pypi.org/project/portmod/)
[![Chat](https://img.shields.io/matrix/portmod:matrix.org)](https://matrix.to/#/!kUmwclOKJPyTSXmXyQ:matrix.org?via=matrix.org)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

A cross-platform cli package manager for mods. Based on Gentoo's [Portage](https://wiki.gentoo.org/wiki/Portage) package manager.

Currently the only supported game is OpenMW, via the [openmw-mods](https://gitlab.com/portmod/openmw-mods) repository.

See [the Wiki](https://gitlab.com/portmod/portmod/wikis/home) for details on [Installation](https://gitlab.com/portmod/portmod/wikis/Installation/Installation) and [Setup](https://gitlab.com/portmod/portmod/wikis/Setup).

## Features

- **Automatic Downloads (where possible)**: If direct links are available to mod archive files, portmod will fetch them automatically. As many mods have restrictive licenses and are distributed via sites which do not provide direct links, this is not always possible.
- **Automatic patching**: Mods are organized into packages which contain both the base mod and any necessary patches. Patches can be configured (in the package) to only be installed when certain other packages are installed, so that all you need to do when installing packages is choose the ones you want and all necessary patches will be included automatically.
- **Automatic Configuration**: Mod packages can declare optional features (called [Use Flags](https://gitlab.com/portmod/portmod/-/wikis/configuration/use-flags)), which can either be independently enabled/disabled (local flags), or enabled/disabled along with other packages which share the same feature (global flags).
- **Structure Awareness**: Portmod's package files contain information about the directory structure of the archives which explain precisely how the mod should be installed.
- **Automatic sorting**: The install order and the load order of plugin and fallback archive files are sorted automatically based on rules defined in the packages. These rules can be customized with [user rules](https://gitlab.com/portmod/portmod/-/wikis/configuration/user-sorting-rules).
- **Automatic updates**: When mod updates are released and new package files are created in the portmod repository, you can find and update all your installed mods using a single command. Due to portmod requiring more information than upstream sources usually provide, will be a delay after the upstream mod is updated while new package files are created.
- **Dependencies**: Portmod will automatically install dependencies for the mods you ask it to install.
- **Mod collections**: Portmod supports both metapackages (packages containing lists of other packages which are distributed in the repository), as well as custom [package sets](https://gitlab.com/portmod/portmod/-/wikis/configuration/sets) (easy to set-up package lists that exist in the user's configuration).

## Installation, Setup and Usage

See the [Guide](https://gitlab.com/portmod/portmod/-/wikis/Home#guide) on the wiki.

## Future Plans

This list is updated infrequently. See the [Issues](https://gitlab.com/portmod/portmod/-/issues) for up-to-date information.

- **Support for other game engines**: Support for other engines is already feasible (portmod's implementation is fairly generic), but restricted by the lack of support for installing into a single data directory. Currently games must support per-mod data directories.
- **Mod packaging and submission**: Support for build files being distributed with mods and automatically submitted to a repository using a cli tool.

## Communication

Release announcements and other major news will be posted to the [announcement mailing list](https://lists.sr.ht/~bmw/portmod-announce)). This list is read-only (see below for the list you can contact).

There are a number of ways to communicate with the developers and with other users:

- [Matrix](https://matrix.to/#/+portmod:matrix.org)
- Mailing List - [Page](https://lists.sr.ht/~bmw/portmod) - [Email](mailto:~bmw/portmod@lists.sr.ht)
- GitLab, via the [Issue Tracker](https://gitlab.com/portmod/portmod/-/issues) and the [email service desk](mailto:incoming+portmod-portmod-9660349-issue-@incoming.gitlab.com)
- [OpenMW Forum Thread](https://forum.openmw.org/viewtopic.php?f=40&t=5875)

[![Packaging status](https://repology.org/badge/vertical-allrepos/portmod.svg)](https://repology.org/project/portmod/versions)
