# Changelog

## [2.0_rc6] 2020-03-04

### Dependencies
#### Changed
- The progressbar2 requirement has been updated to specifically require >= version 3.2.
  There has been no change in terms of the actual runtime requirements, however python
  will now enforce this at runtime so the error message in case its missing will be more
  transparent.

### User Features
#### Changed
- Progressbars will no longer be displayed if portmod's output is redirected.
- the `query uses` subcommand will now differentiate between local, global and use_expand flags.

### Dev Features
- A couple of modules have been made private (`.wrapper` -> `._wrapper`, `.deps` -> `._deps`)
  as well as several functions. These should not be used by external programs.
- Added a `get_flags` function in `portmod.query` which can be used to get (categorized) use
  flag descriptions for all of a package's flags.

### Bugfixes
- inquisitor will no longer produce an error if run without arguments
- Fixed an issue causing both the automatic and manually set texture_size use flags to be
  enabled if you set them manually.

## [2.0_rc5] 2020-02-22

### User Features
#### New
- Added repository and package information to the info command.

#### Changed
- Portmod will no longer check if a package needs to be rebuilt (indicated by it being added
  to the `rebuild` set) if the package is already in the `rebuild` set.
- The `query has` subcommand will now respect the `--quiet` option.

### Dev Features
#### Changed
- Made Pybuild1.S be the fallback to Source.S if it's not set and there is only one source.

### Bugfixes

- Fixed a regression preventing packages from being merged if `--onshot` is used and the
  package has no configuration changes or update.
- Made `--newuse` work even if `--deep` is not specified.
- Fixed a bootstrapping bug preventing the use of multiple repositories.
- Fixed package loading error caused by moving package repositories.
- Fixed updates being skipped if they would cause configuration changes.
- Fixed a sandbox permissions error on MacOS caused by leftover outdated and unused code.
- Fixed detection of superclass files for cache invalidation of pybuilds
- Fixed a bug when using the `query has` subcommand on optional fields.

## [2.0_rc4] 2020-02-07

### User Features
- Added the `installed` set. This can be used to query installed packages
  (e.g. `portmod <prefix> query list @installed`)
- Made some of the query subcommands produce quieter output suitable for scripting when
  `--quiet` is specified.

### Dev Features
- Added `prerm` function to modules so that they can cleanup any changes they've made to the
  system before being removed.

### Bugfixes
- Fixed interface to `inquisitor commit-msg`
- Made local changes to repositories no longer be overwritten when the repository is updated.
  Repositories will be updated with `git pull --rebase`, and may fail to update if there are
  local changes which would create a conflict.
- Fixed the permission of the directory used for the extraction of files from VFS archives
  within the sandbox
- Symlinks created by modules will no longer cause errors when the file they are replacing
  already exists. The last time this was fixed, it actually only fixed symlinks which were
  dangling.
- Fixed packages not being added to `@rebuild` if they were part of the current merge list
- Fixed misattributed flag descriptions in `portmod <prefix> query uses`.
- Fixed a bug preventing inquisitor from detecting missing entries in Manifest files.

## [2.0_rc3] 2020-01-22

### Bugfixes
- Fixed inquisitor-scan hook to match paths which are not in the root of the repository.
- Fixed the `portmod <prefix> validate` subcommand
- Fixed a regression caused by the migration code introduced in 2.0_rc2 to handle a regression
- Fixed explicit rebuilding of sets (e.g. `merge @rebuild`, broken in 2.0_rc2
- Fixed how inquisitor differentiates between category and package metadata files.
- Allowed inquisitor to be run outside repositories as long as a file or directory within a
  repository is passed as an argument.

## [2.0_rc2] 2020-01-20

### Dependencies
- All platforms now require at least version 0.16 of the `fasteners` python library.

### User Features
#### New
- Mods can now be manually installed in  `$PORTMOD_LOCAL_DIR/pkg/local`.
  Any subdirectories of this directory will be included automatically in the VFS, and recognized
  by modules such as openmw-config (plugins and archives are registered based on patterns
  included in the profile configuration).

#### Changed
- The downlaoad progress bar now includes an indication of the total downloaded.
- Portmod can now safely be run in multiple processes simultaneously. A inter-process lock will
  ensure that only one process can perform modifications to the system at a time.

### Package Features
#### New
- An inquisitor pre-commit hook is now provided for checking files in package repositories.
- Inquisitor can now produce commit messages via `inquisitor commit-msg` (and a pre-commit
  hook for this is also included).

#### Changed
- `inquisitor`'s interface has been overhauled so that it can process individual files or
  directories instead of only handling the entire repository at once.
- The `pybuild` command has been removed in favour of `inquisitor`. `pybuild <file> manifest`
  has been replaced by `inquisitor manifest <file or files>`, `pybuild <file> validate` has
  been replaced by `inquisitor scan <file or files>`, and the other operations it
  provided were broken and unused anyway.

### Bugfixes
- Symlinks will no longer be created when setting up the sandbox if they are within a directory
  tree which already has read permissions
- Symlinks created by modules will no longer cause errors when the file they are replacing
  already exists.
- The dangling entry point `openmw-conflicts` has been removed. Note that its functionality
  was moved previously to `portmod <prefix> conflict-ui`.
- Fixed directory used for the storage of warning and informational messages produced by
  packages during installation, which wasn't given correct permissions in the sandbox.
- Augmented assignment of attributes in packages (e.g. `self.DEPEND += " ..."`) will no longer
  raise an exception indicating that the feature is disallowed.
- Fixed a bug where selected packages would be added to/removed from the wrong file. Migration
  code has been included to combine the incorrect file with the correct one.
- Packages will no longer be re-configured, updated or downgraded when the `--depclean` option
  is used.
- Fixed a bug in the installation of packages which contain symlinks.
- Made sure that, when explicitly rebuilt by passing the package name on the command line without
  the noreplace option, packages will always install using the repository version, not the
  installed version.
  Installation using the installed version is still slightly buggy, and is now only possible if
  it is the only version available.

### Localization
- A few Swedish (sv-SE) localizations were added by @edvind

### Internal Changes
- A number of operations have been cached to improve performance

## [2.0_rc1] 2020-12-24

### Bugfixes
- Fixed support for python3.6, broken in 2.0_rc0
- Fixed handling of unicode characters in pybuild files, broken in 2.0_rc0
- Fixed support for statically linked versions of python/git/bsatool.

## [2.0_rc0] 2020-12-22

This release makes several breaking changes to the way portmod stores and processes package files and
installed mod packages. There is a migration tool included, which will run the first time you run any
portmod command, and should make the change to the new version smoother by moving a number of
files and directories.

After running the migration tool, installed packages will still be broken, so you will need to
run `portmod sync`, followed by `portmod openmw merge -uDN @world`, and let all your packages
be re-installed (noting that the migration tool will by default create a prefix named `openmw`,
though you can change this, and your choice will replace `openmw` in the command).

### User Features

#### New
- Portmod now supports multiple independent configurations, called prefixes, making it possible
  for portmod to manage multiple different games, or different configurations of the same game.

#### Changed
- The CLI has been rewritten to be more centralized. A single executable, `portmod` is now used,
  with various subcommands. `<prefix>` is the name of the prefix you are using.
  - `portmod <prefix> merge` replaces `omwmerge`
  - `portmod <prefix> search` replaces `omwmerge -s`/`omwmerge -S`
  - `portmod <prefix> query` replaces `omwquery`
  - `portmod <prefix> select` replaces `omwselect`
  - `portmod <prefix> use` replaces `omwuse`
  - `portmod <prefix> conflict-ui` replaces `openmw-conflicts`
  - `portmod sync` replaces `omwmerge --sync`
  - `portmod mirror` replaces `omwmirror`
- How portmod handles sets has been overhauled. Notably, the contents of a set will no longer be
  selected when you install using the set instead of a package name.
  Instead, sets (excluding builtin sets) will be marked as selected, and their contents will be
  considered part of the `@world` builtin set.
- Several user-facing files in the portmod config folder (shown by `portmod <prefix> info` as
  PORTMOD_CONFIG_DIR) have been moved:
  - The user configuration directory is now divided into subdirectories for each prefix, with all files, unless otherwise specified, having moved into the prefix-specific subdirectories.
  - Non-prefix-specific settings can be set in a `portmod.conf` file in the root of the config dir.
  - `mod.use` has been renamed to `package.use`
  - `mod.accept_keywords` has been renamed to `package.accept_keywords`
  - `repos.cfg` has not moved
- The installed packages directory has been moved to `$PORTMOD_LOCAL_DIR/<prefix>/pkg`

### Package Features

#### New
- Packages can now be renamed/moved using the `move` command in files in the `profiles/updates`
  directory.

#### Changed
- The `Mod` class has been renamed to `Package`
- `pyclass` has become `common`, and has a stricter structure. Imports need to be from specific
  submodules (e.g. `from common.git import Git`), which are themselves packages, so that the
  imports work properly when some are defined in different repositories.
  Packages also depend on the specific version of the common packages they used at the time of
  installation, so any updates to the common package will require that the packages using them
  are rebuilt.
- Certain package variables and functions have been renamed:
  - `M` -> `P`
  - `MF` -> `PF`
  - `MN` -> `PN`
  - `MV` -> `PV`
  - `MR` -> `PR`
  - `MVR` -> `PVR`
  - `mod_nofetch` -> `pkg_nofetch`
  - `mod_pretend` -> `pkg_pretend`
  - `mod_prerm` -> `pkg_prerm`
  - `mod_postinst` -> `pkg_postinst`
- `pybuild.modinfo` has been renamed to `pybuild.info`
- The `REBUILD` pybuild variable has been removed, and replaced with a `REBUILD_FILES` variable,
  which supports a list of fnmatch-style patterns. Changes to files in the VFS matching any
  of these patterns will cause the package to be marked as needing to be rebuilt.
- The `ARCH` variable is now set by the prefix rather than the profile, and is included as
  a profile variable by default (and thus can still be referenced within the profile).

### Bugfixes

Portmod is now [mypy](https://github.com/python/mypy)-compliant, which fixed many bugs and
potential bugs. This, combined with the major changes to features, means that it would be
difficult to meaningfully enumerate bugfixes for this release. Full listing of bugfixes will
resume in the next release.

### Internal Changes

- Sandboxing is now done entirely out of process. The sandbox systems previously used just for
  executing arbitrary commands during installation (bubblewrap, sandbox-exec, Sandboxie) are
  now used to sandbox the entirety of pybuild loading and execution.
- Blake3 is now the default hash function used in Manifest files.
- MD5 hashes will no longer be checked unless they are the only hash function present, as
  we only generate them for comparison against certain other sources (Google download
  servers and the NexusMods API).

## [2.0_beta8] 2020-09-29

### Dependencies
- Black, a dependency used in development, has been declared as a dependency in setup.py
  despite not being used at runtime. It has now been removed from the dependencies enforced
  by setup.py.

### Changed User Features
- The default openmw repository is only added to the list of repositories used internally
  if repos.cfg does not exist. This means that it can be disabled, and also that if you've
  modified repos.cfg and removed the openmw entry, the default repo will no longer be used.

### Bugfixes
- Fixed the subcommand descriptions for the `omwquery` command.
- Repositories are now identified solely by the name stored in `profiles/repo_name`.
  The section name in repos.cfg is only used to identify the repo within that file.

## [2.0_beta7] 2020-09-03

### Dependencies
- Portmod now requires the python packaging module (https://github.com/pypa/packaging/ ).
- Portmod now requires the importlib_metadata module when python 3.6 or 3.7 is used.
  https://gitlab.com/python-devs/importlib_metadata/
- The argcomplete module can optionally be used to provide tab-completion in bash and
  certain other shells.

### User Features

- Portmod now provides internationalization. Currently the only localizations not
  matching the fallback locale (en-GB) are strings which have different US spellings.
- Import overhead has been reduced, resulting in less delay when executing portmod's
  scripts.
- Added more messages during installation to display the beginning and end of the
  various installation phases.
- The Temporary directory will now be cleaned up in its entirety at the end of installation.
  Previously this would be done only for specific directories, meaning that failed installs
  would never be automatically cleaned up.
- A warning will be displayed if the Temporary directory may be too small.

### Dev/Pybuild Features

- InstallDir.BLACKLIST and InstallDir.WHITELIST now accept fnmatch-style patterns, which
  include the * and ? operators, as well as ranges like [1-9]
- Directory names within repository categories are now checked by inquisitor to make sure
  that they match the names of the pybuild files themselves.

### Bugfixes
- Fixed bug in how disabled use flag dependencies (e.g. foo[-bar], i.e. foo with flag
  bar disabled) are parsed. Previously the "-" was being included as part of the flag
  in dependency resolution.
- Made conflicts with REQUIRED_USE clauses not show the REQUIRED_USE string twice if the
  part causing the conflict is the same as the entire string.
- Fixed bug which displayed duplicated use flag dependencies in dependency conflict atoms.
- Fixed a few version comparison bugs
  - Multiple suffixes weren't being handled properly
  - The result was sometimes incorrect for versions with different numbers of numeric
    components (e.g. 1.0 and 1.0.1)
- Fixed dependency resolution to give the same weight to each equal versions, regardless of
  repository
- Made use expand flags be set before other flags so that they can be disabled via profiles
  and user-configuration, rather than overriding them.
- Made environment variables always override use flags from other sources.
- Pybuilds are now always explicitly loaded as utf-8, rather than using python's locale-based
  encoding.
- Fixed bugs in how logs were handled which were causing pytest to sometimes fail.
- News in newly added repositories is now considered old news and automatically skipped.
  Previously it would only be skipped if the user had not yet selected a profile, which only
  works for skipping news when portmod is first set up.
- Fixed regression in how archives are handled when passed to omwmerge.


## [2.0_beta6] 2020-07-16

Identical to 2.0_beta5 other than deployment fixes.

## [2.0_beta5] 2020-07-15

### Dependencies
- Portmod now requires rust 1.39+ (https://www.rust-lang.org/) and setuptools-rust
  (https://github.com/PyO3/setuptools-rust) as build dependencies in place of
  omwcmd and pyyaml. Portmod uses these to build a native rust library. Note that the
  rust compiler is not required if you install portmod via pre-compiled wheels.

### User Features
- Dependency conflicts due to forced use flags (e.g. profile required use flags in
  use.force) are displayed more clearly.
- omwquery now has the subcommands:
  - meta (prints package metadata)
  - hasuse (prints packages which make use of a given use flag)
  - uses (displays use flags and their descriptions for a package)
  - depgraph (displays all potential dependencies for a package, and the dependencies of
    those dependencies, etc.)
- Downloaded sources in the user's Downloads directory will be automatically detected
  and moved into the portmod cache if they are not already present in the cache.

### Pybuild/Dev Features
- The `pwinreg.read_reg` function (Windows-only) now returns a dictionary if the key
  has subkeys. Note that this may not work properly with registry keys that contain
  both values and subkeys.
- Profile variables are no longer exported as environment variables (thus preventing profiles
  from being able to override sensitive environment variables such as `PATH`).
- VFS Archive support has been added, meaning vfs lookups via `find_file` now return
  (extracted) paths to files within archives defined in InstallDir.ARCHIVES.

### Bugfixes
- Symlinks in paths are now resolved when validating sandboxed i/o. This fixed an error in
  macOS, which usually has symlinks in the path of the temporary directory.
- Fixed missing quotation mark in the sandbox-exec command on osx (regression in recent release).
- Added additional paths and permissions to sandbox-exec to allow certain executables
  to execute properly (specifically tested perl and git).
- VFS lookups, which had been done in reverse incorrectly, have been corrected.
  This bug was introduced via a regression in the previous release.
- Fixed certain operations on ignoring REQUIRED_USE on File objects defined in InstallDirs.
- Sandboxed executables on Windows now properly return stdout and stderr (if pipe_output or
  pipe_error, respectively, are passed to execute).
- Fixed sandboxed executables on Linux having network access by default (regression
  introduced in previous release)
- Fixed bugs in the display of USE_EXPAND flags in the transaction list which omitted
  certain flags.
- Fixed bugs in the texture size selector causing exceptions when `>=` or `<=` operators
  result in no textures matching the selector function being available (the correct behaviour
  is to fall back to the closest texture size to the threshhold).
- Fixed a bug that would raise an exception when processing module changes to whitelisted files.
- Fixed a bug in dependency resolution which would cause seemingly random changes to use flags.
- Fixed the weighting of globally set USE_EXPAND flags such that they have higher
  priority in dependency resolution than the default values of the flags (as global
  use flags set via the USE variable already have).
- Fixed bug in how packages are removed from the `rebuild` set. Previously, packages
  would be removed even if the build failed.

## [2.0_beta4] 2020-06-12

### Bugfixes
- Fixed bug where inquisitor was incorrectly inserting the repo it was running inside of
  into the repository list and the python path, causing errors if the repo was not
  declared in repos.cfg.

## [2.0_beta3] 2020-06-12

### Dependencies
- Portmod now requires chardet (https://pypi.org/project/chardet/)

### User Features

#### New
- `--quiet` argument has been added to omwmerge, which suppresses most nonessential output
- Warnings and informational messages will be summarized for the user at the end of mod
  installation.

#### Changed
- The config system has been replaced with a simplified VFS system and a module system to
  allow repositories to handle global updates such as config sorting.
  Functionally this  means that updating openmw.cfg has been delagated to
  https://gitlab.com/portmod/openmw-config, which is available as `modules/openmw-config`
  in the openmw-mods repository (will be required by default).
  Certain modules can be configured using omwselect.
- `--verbose` now displays a certain amount extra output that is normally suppressed

### Pybuild/Dev Features

#### New
- The use of `super` is now allowed in the sandbox, and is recommended when overriding
  functions. (e.g. you should call `super().src_prepare()` at some point in `src_prepare`).
  Note that `super().__init__()` is injected into the code, given that `__init__` cannot be
  called manually from within the sandbox.
- The `chardet` module has been added to the sandbox for detecting the encoding of text
  files.
- Module system has been added which allows for custom configuration after installation,
  as well as automatic global updates when new packages are installed or removed.
  See https://gitlab.com/portmod/portmod/-/wikis/Modules

#### Changed
- Instead of `LIVE = True`, live pybuilds (those that depend on a source which may change at any
  time, such as a git branch) should set `PROPERTIES = "live"`.

### Bugfixes
- inquisitor will no longer allow dependencies in packages if they do not exist somewhere
  in the repository or its master repositories.
- Fixed bug which would cause an exception when installing a mod that just symlinks to
  an existing installation when attempting to get the size of the installed tree.
- Fixed a bug in the python sandbox where trying to use our custom safe importer breaks
  modules which are whitelisted.
- Fixed calls to `exit` to use `sys.exit` instead. `exit` may produce a dialogue
  confirmation and is designed for interactive shells only.
- Fixed regression where we would fail to download a file if we cannot find it in the
  first mirror tried, without checking other mirrors or the original URI.
- Removed dependency on the python `patch` module. We never needed it.
- Fixed the FILESDIR not being accessible in src_unpack.
- Corrected the call time of mod_postinst to occur after the final install, instead of
  immediately after src_install.
- Corrected permissions in the sandbox to refer more specifically to the directories
  which are supposed to be accessed. E.g. allowing access to just the build directory
  rather than the entire temporary directory.
- `omwmerge` without arguments now exits with status code 2, rather than code 0.
- Fixed bug where an exception would be raised if the file reffered to by a File object
  did not exist in the InstallDir's directory during src_install.

## [2.0_beta2] 2020-04-23

### Bugfixes
- Fixed download bug where we would download status page when receiving an invalid
  status code.
- Fixed bug when parsing empty licenses, which are valid as of 2.0_beta1.

## [2.0_beta1] 2020-04-18

Note it is recommended that users re-install their mods if they do not use a
case-insensitive file system, as we now support case insensitive file installation.
See the news article `2020-04-14-case` for details (you can use `omwselect news`
to interact with the new news system).

### Dependencies
- pytest-runner is no longer required as a dependency (it really shouldn't have been).

### User Features

#### New
- The sizes of the work directory and the installed tree are now displayed after each
  mod has been installed.
- Use flag requirements (e.g. base/morrowind[tribunal]) are now supported on the
  command line.
- A news module has been added to `omwselect`, which allows you to read, and mark as
  read/unread, news distributed via mod repositories.
- The `--emptytree` option has been added to omwmerge, which will re-install every mod
  in the dependency tree for the given atoms.
- Downloads will now be retried automatically when they fail, though at most once if
  the server doesn't provide the `X-Goog-Hash` header.

#### Changed
- The Transaction list will now always be printed, even if `--no-confirm` is used.

### Pybuild/Dev Features
- Use flag requirements can now be specified in DATA_OVERRIDES
- Mod installation can now be done in a case-insensitive manner
  (i.e. when combining multiple trees in the install phase, files with the same name but
  different case will overwrite each other). This is enabled per-repository using the
  CASE_INSENSITIVE_FILES boolean setting.
- The list file parser will now skip empty lines, meaning that files with empty lines
  will no longer cause errors.
- `version_gt` can now be used in the sandbox, and is exported in the pybuild module.
- Pybuild.execute now accepts the option `pipe_error`, which allows redirection of
  stderr separately from stdout.
- Pybuild.execute will parse output as a string if output is redirected.
- Dependencies on atoms in the `sys-*` categories will no longer be ignored by the
  dependency solver.
- The `~` operator is now supported for atom matching (matches the given version,
  but any revision, unlike `=`, which matches only the specific version given)
- The `mod_pretend` function has been added, which is called prior to user
  confirmation when installing. and can be used for validation checks prior to the
  main installation phase.

### Bugfixes
- Directories in mods that are identical other than case will now be merged during
  installation if CASE_INSENSITIVE_FILES is set in the config.
- Cached pybuilds use the proper repo name, rather than always showing the
  "installed::installed" repo
- Fixed Exception raised by progressbar when adding new files to the manifests
  (introduced in beta0)
- Suggested changes to mod.accept_keywords now specify the revision, as well as
  package version, rather than suggesting atoms that don't match the target if the
  revision is greater than 0.
- get_restrict now works on mods loaded from the cache, fixing the omwmirror script.
- Atoms with use flag dependencies are now blocked only if those dependencies are met.
- Dependency weighting has been reworked, and the `newuse`, `update` and `depclean`
  options are more tightly integrated into dependency resolution to ensure that
  the results are sane.
- The loader will now load all files in all categories that match the atom, not
  just those in the first category encountered. I.e. we will properly recognize
  atoms which are ambiguous due to existing in multiple categories.
- Use expand parsing when displaying the transaction list has been fixed. Some
  flags would not be displayed as enabled, even if they were.
- When sorting the install order, runtime dependencies of build dependencies are now
  merged ahead of the mod with the aforementioned build dependency (i.e. a build
  dependency means we want to use that during the build process, and its runtime
  dependencies may be necessary for this to work).

## [2.0_beta0] 2020-04-02

### Dependencies
- Development versions of Portmod require setuptools_scm at runtime for fetching
  version information.
- All versions require python-sat
- Python 3.7 64-bit or 3.8 64-bit is required on Windows, as these are the only
  pre-built wheels available for python-sat. Additionally, python-sat must be
  version 0.1.5.dev4.
- Microsoft Visual C++ Redistributable is required on Windows (necessary for
  python-sat pre-compiled wheels).
- Portmod will now make use of the libyaml backend of PyYAML if it is available
  (see https://pyyaml.org/wiki/LibYAML )
- The python package "requests" is now required on all platforms.

### User Features

#### Added
- Comments (beginning with #) are now supported in mod.use, mod.accepts_keywords
  and similar files.
- Local archive files can now be passed on the command line to omwmerge.
  These files will be moved to the cache directory, and portmod will install the
  mods they correspond to.

#### Changed
- Portmod will now handle dependencies more intelligently and display conflicts
  more verbosely. Most use flag changes that are required to avoid conflicts will
  now be detected automatically.
- Portmod now caches pybuilds to speed up most operations significantly.
- The config will now only be sorted at the end of mod installation, or as needed
  when a build file accesses the VFS.

### Pybuild/Dev Features

#### Changed
- Pybuild files should now import from `pybuild` module rather than
  `portmod.pybuild`. The current behaviour will be supported at least until
  v2.0
- Portmod now uses thin manifests that only contain DIST entries. As such, you
  now only need to run `pybuild file.pybuild manifest` when a pybuilds source
  archives have changed.
- Repositories now declare their master repositories in the file
  `metadata/layout.conf`. This file uses the same format as other python-like
  config files, and masters should be a whitespace-delimited string list of
  repository names. E.g. `masters = "openmw openmw-testing"`
- The DESC field is now reflowed such that newlines are replaced by spaces. I.e.
  you can add newlines to maintain proper line length, without affecting how
  they are displayed in search results (note that descriptions longer than one
  line are discouraged).
- AA (list of all mod sources) Has been removed. It was not used and was deprecated
  in eapi 7 (see PMS).
- File.MASTERS (alias of File.OVERRIDES) has been removed.
- Manifest files now only store entries for DIST files.

#### Added
- The beginnings of a stable interface is now being provided via the root
  portmod module (now that it is no longer part of the pybuild import tree).
  These functions will be maintained between major versions of portmod such
  that any dependent software/scripts does not break when portmod updates.
- Field values in field-based config entries are now stringified. Practically,
  this means you can now use integers as values when specifying config information
  in pybuild fields such as FALLBACK.
- File and InstallDir objects now are stringified in a manner similar to how they are
  created. E.g. `InstallDir("path", REQUIRED_USE="foo")`
- hasattr and getattr can now be used inside pybuilds.
- Added UNFETCHED variable to pass sources that need to be fetched to mod_nofetch
  function.
- File.OVERRIDES can now be a list of files (makes it possible to handle files
  containing spaces). Old functionality of being a string that can contain use
  conditionals has been maintained.
- Added the builtins of next, iter, filter, map, max, min, dict, enumerate, sum,
  any, all, reversed and sorted to the sandbox
- Blockers can now be included in the DATA_OVERRIDES fields to indicate underridden
  mods.

### Bugfixes
- Fixed fetching portmod version information for development versions (i.e.
  when there is no installed python egg info).
- Fixed a bug which may cause sorting mods to report cycles incorrectly due to
  the code attempting to trace cycles via empty nodes.
- Fixed some bugs in how use flags are displayed for mods, caused by empty lists
  (e.g. when no flags are enabled) being treated the same as the special case of
  None.
- Fixed bug where portmod would interrupt downloads directly into the cache for
  files that contain spaces by renaming the file prior to it having finished
  downloading.
- Exceptions will no longer be raised if a mod's installation does not exist
  when a mod is removed (e.g. due to a previous error).
- Read-only files will be removed properly when uninstalling mods and cleaning up
  the temporary directories during installation.
- The portmod.conf placeholder file will always be created when portmod is invoked.
  previously it would not prior to profile selection.
- Fixed error when displaying licenses the user needs to accept.
- Portmod will no longer throw exceptions when initializing with a version of
  GitPython less than 3.0.5.
- Fixed issue where we were failing to download files from the gitlab-based file mirror.
- Pybuild files can no longer install to arbitrary paths by using chains of `..` in
  PATCHDIR to escape the build directory.

## [2.0_alpha6] - 2020-01-28

Note that one of the bugfixes changed the data directory produced by
base/morrowind. If you previously had this installed, you will need to
manually remove the old data entry from openmw.cfg (`omwmerge --sort` will
produce a warning about the line).

### Dependencies
- Windows now requires [Sandboxie](https://www.sandboxie.com/).
- All platforms now require [RedBaron](https://github.com/PyCQA/redbaron)

### User Features
- Windows: Replaced SANDBOX_COMMAND with automatic sandboxie configuration.
- Added `--nodeps` argument, which can be used to ignore dependencies when
  installing. Note that this is designed for debugging purposes, and may
  cause mods to fail to install, or fail to work if their dependencies are
  missing.

### Pybuild/Dev Features
- Added support for raising errors when stderr is printed to in the sandboxed
  execute function
- Added support for in-place variables to the sandbox. I.e. +=, -= type
  operations can now be used in Pybuilds.
- Added _unpack_sequence_ to sandbox. I.e. `a, b = "baz".split("a")` now works
  in the sandbox
- portmod.query.query now optionally takes multiple fields, and outputs as a
  generator function
- Added list_dir function for scanning for vfs files
- Added utility functions to Pybuilds for getting enabled Files and InstallDirs

### Bugfixes
- Added requirement that RestrictedPython be >= 4.0 to setup.py.
  This had been previously documented, but not enforced.
- Replaced configparser with redbaron to fix automatic modifications to user
  config. This had been broken since the introduction of the python-based
  config file
- fixed display of USE_EXPAND type flags in searches and transaction list
- Fixed how omwcmd dependency is handled in CI to ensure we aren't spending
  unnecessary time re-building it.
- Fixed Windows path issue where profile path would be malformed
- Fixed Windows bug where mod could not be uninstalled due to attempting to
  remove the current working directory.
- Fixed bug where we were replacing spaces with underscores in fallback section
  values, in addition to the keys and section names (where it's necessary).
  Fallback entries now match what is produced by the openmw-iniimporter
- Made symlinks be resolved when producing path to include in config files.
  This means that the data entry in openmw.cfg generated by base/morrowind will
  now match the one generated by the openmw-wizard, meaning that, with the
  previous bugfix, the wizard will no longer cause problems if run before portmod.
- Made sure that we create parent directories for config files if they do not exist.
- We no longer block module imports for the pyclass module, as it is entirely
  sandboxed. This was done since the code for blocking modules requires running
  the module outside of the sandbox, code indended for use with system modules which
  are trusted, not untrusted modules like pyclass.
- Setuptools now enforces the need for RestrictedPython>=4.0 via setup.py
- Repo name parsing in Atoms now matches the PMS, and doesn't consume USE flag conditions
  if both are provided.

## [2.0_alpha5] - 2019-12-24

Small release, primarily to fix a significant bug introduced in previous version.

### User Features
- Made display of included source directories be unambigous (previously relative
  directory paths were shown, but not which archive they came from if there are
  multiple archives).

### Bugfixes
- Fixed bug that would prevent mods with `RESTRICT="fetch"` from being installed.
  Introduced by changes to fetchability detection in v2.0_alpha4.

## [2.0_alpha4] - 2019-12-23

Biggest release yet, largely since it's long overdue.

### Windows Support
After support for Windows having lapsed after the introduction of the sandbox,
various Windows bugs have now been resolved, Windows CI has been introduced, and
it *should* mostly work now.

Two issues are outstanding:
- Executable sandboxes are still shaky. Theoretically, [sandboxie](https://www.sandboxie.com/),
  which is now free, and soon to be open-source, could be used. Currently adoption
  is limited by its current EULA preventing any sort of installation in the CI
  environment. Users are welcome to try and get it to work, providing the
  appropriate `SANDBOX_COMMAND`, otherwise, Portmod will now inform you of
  commands that are being attempted (so you can check that they're benign)
  and prompt you to allow them to run without a sandbox.
- There is an unknown bug showing up in CI where files are unable to be deleted
  due to "being used by another process".

### User features
- Added support for [user config sorting rules](https://gitlab.com/portmod/portmod/-/wikis/Configuration/User-Sorting-Rules).
- Cycle detection when doing dependency resolution and sorting the config is now
  more verbose
- Added support for no-argument depclean (i.e. `omwmerge --depclean`) to remove
  mods that were pulled in as dependencies but are no longer needed. They can be
  removed automatically using the `--auto-depclean` or `-x` flag when performing
  other operations.
- Added `OMWMERGE_DEFAULT_OPTS` environment variable to allow the use of default
  options that are always passed to `omwmerge`. `--ignore-default-opts` can be used
  to override this.
- Windows users will be prompted if they have not set `SANDBOX_COMMAND` and install
  a mod that requires external executable calls.
- Housekeeping operations (sorting, updating the VDB, etc.), are now performed even
  if mods fail to install.
- We now track when the config needs to be sorted, and if necessary will retry
  sorting even if no other operations need to be performed.

### Pybuild/Dev features
- The `pwinreg` module has been added, providing a read_reg function for reading
  values from the Windows registry, as well as `HKEY_` constants from `winreg`.
- The "fetch" and "mirror" `RESTRICT` values are no longer recommended to be used
  in Pybuilds, as new smarter behaviour detects if mods can be fetched or mirrored
  using the mod's license and uri.
- `src_unpack` can now be used for manual unpacking of mods. To assist this, an
  `unpack` function has also been added.

### Bugfixes
- Mods only available in the installed DB can now be re-installed (also fixed in
  last release... This time for sure!)
- Fixed how we remove entries that use indices (the `i` variable) in ini-type
  config files.
- The downgrade transaction is now used where appropriate.
- The config path is now properly expanded when accessing the VFS.
- Various names (not used) which are not available on win32 have been removed from
  the sandboxed os module.
- Sandbox now has access to `/run` and `/etc`, which is necessary for git calls.
- Display of maintainers in search results has been cleaned up, and no longer
  throws an exception if there are multiple maintainers.
- USE_EXPAND has been fixed, and now behaves like it does in Portage.
- When removing test directories (which may contain read-only files that cannot
  be otherwise removed on Windows), we now give write access to files that fail
  to be deleted, before retrying.
- Added an extra layer of backslashes to backslashes on Windows in files handled
  by the sandbox (unknown why this is necessary).
- Added workaround for upstream python Windows Pathlib bug (https://bugs.python.org/issue38671)
- Removed shlex for subprocess calls on Windows, as they are not needed and
  cause errors on Windows.
- Cleaned up how we handle trailing junk in mod directory paths so that they
  are normalized in a cross-platform way.
- Default values for user.name and user.email are now provided for the git
  repository in the VDB (note that this repo is for internal use, so these
  values don't need to be correct).
- Config sorting is now performed after each mod is installed (instead of
  once at the end) to ensure that it always reflects the current state of
  the installation, since it may be used by mods for VFS lookups.
- The FileNotFoundError exception is now provided by the sandbox.
- Fixed bug when comparing versions of an installed mod with an updated version.

## [2.0_alpha3] - 2019-09-08

### Dependency changes
- Now requires omwcmd 0.2
- `dcv` is no longer a dependency (undocumented requirement of the
  `openmw-conflicts` executable)

### User Features
- `omwmerge --info` now only displays a useful subset of config variables.
  Full set can be viewed by also passing `--verbose`.

### Pybuild/Dev Features
- `InstallDir.SOURCE` has been deprecated in favour of `InstallDir.S`, which
  refers to the extracted archive name (without extension).
- USE_EXPAND support. Notably allowing nice localization support through the
  L10N config variable.
- Inquisitor will no longer allow mods names that end in a version component,
  which are invalid as they cannot be properly parsed.

### Bugfixes
- Fixed bug in detecting which files we can detect masters from that meant we
  previously were ignoring masters for all files.
- Fixed handling of environment variables to override config variables.
- Fixed depcleaning mods that include blockers (`!!`).
- Made updates be shown as update transactions rather than new mods even if the
  update option is not passed.
- Fixed reinstalling mods from DB if mod is no longer available.
- Mods with revision numbers (E.g. `cat/foo-1.0-r1`) no longer cause an exception
  to be thrown when encountered.

## [2.0_alpha2]- 2019-08-11
### Bugfixes
- Fixes second setuptools_scm issue.

## [2.0_alpha1] - 2019-08-10

### Bugfixes
- Fixed incorrect Download link on Pypi and issue with the Portmod update
  detection mechanism (which warns if a repository is marked as using a newer
  version of Portmod than is currently installed).

## [2.0_alpha0] - 2019-08-10

First Alpha release of Portmod 2.0
