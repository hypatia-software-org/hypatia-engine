# Changelog

Uses http://keepachangelog.com/ as a guideline.

## [0.2.24] - 2015-07-13

### Added

  * `readme` Python module for testing PyPI rst readme/PKG-INFO

### Fixed

  * `readme` for PyPI, according to `readme` module

## [0.2.23] - 2015-07-12

### Changed

  * `README.md` can now be auto-converted to rst for upload to PyPi. PyPi doesn't allow internal or relative links.

### Fixed

  * `test.sh` will generate `PKG-INFO` for `setup.py`

## [0.2.22] - 2015-07-12

### Added

  * `distrib.sh`: for PyPI distribution automation
  * `setup.py` long description, which works in combination of above

### Changed

  * `AUTHORS.md`: brief description of user contributions and James Leung
  * sphinx setup; using a more standard "docs" and "docs/build" approach
  * `make-sphinx.sh` for the above reason

## [0.2.21] - 2015-07-12

### Added

  * `etc/` directory with pre-push test script, thanks @ejmr! See pull request #49.

### Fixed

  * doctest for python 3 in `util.Resource`

## [0.2.20] - 2015-07-12

More cleanup/fixes.

### Changed

  * Docstrings for `util.Resource`, they're a lot better now
  * Cleanup

### Fixed

  * Was using basename to set filename for files in Resource

## [0.2.19] - 2015-07-12

Cleaning up!

### Chanegd

  * `Velocity.get_diretion` simplified, made modular
  * `util.Resource.__init__` has a new way of loading files, each file extension is associated with a callback function for providing a desired object based on file string or bytes.

### Added

  * properties added to Direction class: x, y, cardinal
  * `util.configparser_fromfp()`

### Fixed

  * `Direction.__add__`, `load_gif()`, `pil_to_pygame()` docstrings

## [0.2.18] - 2015-07-12

Scenes now read through Resource class.

### Changed

  * debug scene now a zip as per Resource class
  * game.Scene uses Resource class to load the debug zip from the scenes resources directory.
  * Resources will hold non-configuration text files as strings, rather than StringIO
  * test_tiles.py needed to be updated to use new Resource system so it could read a tilemap from a scene zip archive/resource.

## [0.2.17] - 2015-07-10

### Fixed

  * Whoops! Merged #51: emums not unique! Thanks, @ejmr.

## 0.2.16 - 2015-07-09

Whoops! How did I not notice the indentation problem in actors.py before?

### Fixed

  * Spacebar caused 0.2.15 to crash. This was because of an indentation error in actors.Actors.

## [0.2.15] - 2015-07-09

### Added

  * Yet more badges to the readme
  * Velocity
  * Velocity to Actor class, defaulting to 20
  * `__contains_` magic method to Resource
  * logo notes

### Changed

  * Misc. corrections to documents, e.g., readme
  * `test.sh` to launch the game demo after running tests
  * completely changed the Direction Enum, renamed class atributes of Action to
    lowercase
  * demo game resource walkabouts repackaged to support new directions. changed
    from up to north, etc.
  * moved the say method from npc to the Actor class
  * updated all docstrings to reflect changes, updated all code to support new
    Direction and Velocity.

### Removed

  * speed from Walkabout class. added velocity to Actor class.

### Fixed

  * Resolved issue #50 where walkabout children would not render, because
    anchors_ini never got loaded, due to incorrectly looking for the associated
    ini file. Noteworthy: this issue had been present for several releases
    without notice!

## [0.2.14] - 2015-07-07

Hey sweet stuff,

I've been sitting on this update for a little bit. It's mostly documentation-oriented. Although, I did a fair amount of reworking of the requirements and install system.

With Love,
Lillian Lynn Lemmer

### Added

  * Added media directory, and put some logos in it. New, updated logos, icons. Put xfc and pngs.
  * CONTRIBUTING
  * AUTHORS

### Changed

  * Fancier changelog
  * minimal rest markup in docstrings, sphinx-source changes
  * travis ci config
  * requirements setup
  * repo document filenames (changed)
  * converting documents to markdown
  * Actor module docstrings enhanced

### Fixed

  * Fixed install scripts to use new requirements location

## [0.2.13] - 2015-07-05

Hello Lovelies,

Here's what's new in 0.2.13:

  * Introduced "Contributor Code of Conduct" as code-of-conduct.adoc.
  * All resources are kept in a zip and managed through the Resource class now. Well, except for scene. I'll get to that next update.
  * Renamed "sprites" to "animations," and reflected that change in all modules.
  * Organization--moved the cycle palette and load gif from file functions to the animations module, reflected changes in various files
  * General cleaning, massive docstring updates
  * sphinx-source for auto-building api docs, also sphinx build script +make-sphinx.sh+.
  * new util module
  * fixing test.sh (was installing from pypi, not local!)
  * resolved current directory issue with tests

And who knows what else!

With Love,
Lillian
