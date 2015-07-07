# Changelog

Uses http://keepachangelog.com/ as a guideline.

## [Unreleased] - Unreleased

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
