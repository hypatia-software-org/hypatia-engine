# Changelog

Uses http://keepachangelog.com/ as a guideline.

## [0.3.4] - 2015-11-16

### Added

  * New demo GIF.
  * `scripts/install`, a new script for bootstrapping the engine, which is a simplified version of the now-removed `scripts/bootstrap`.
  * FreeBSD, NetBSD, and OpenBSD installation support.
  * Linux Mint support.
  * "Scenes" which the engine can `render()`.
  * A new anchor system for animated sprites.
  * Sprite-groups have walkabout information to help animate NPCs.
  * Windows test script supports Python 2 and 3.
  * Script that generates documentation using Sphinx uses the developer's preferred browser.
  * Shell environment variables to control which version of Python the engine uses:
    - `PREP_COMMANDS`
    - `PREP_COMMANDS_PYTHON_2`
    - `PREP_COMMANDS_PYTHON_3`
  * The test script uses `$PAGER`.

### Fixed

  * All unit tests pass.
  * Multiple bugs preventing Python 3.5 from running Hypatia.
  * Doctests and PEP8 style errors in many modules.
  * Actors cannot `talk()` if they do not have the necessary properties.
  * `setup.py` correctly handles the `enum34` package as a dependency based on the version of Python used to install Hypatia.
  * README has correct URLs for images.
  * `Direction.from_velocity()` works for directions with zero values for position coordinates.
  * Hypatia reads UTF-8 encoded text resource files properly.
  * Math on `Anchor` objects is associative and commutative.
  * Various typos in documentation.

### Changed

  * Contribution guidelines.
  * All exceptions related to the `Actor` class have a new parent, `ActorException`, instead of deriving directly from `Exception`.
  * Running the (non-Windows) test script forcibly reinstalls all dependencies.
  * Installation script learned the `--travis` flag for better Travis-CI configuration.
  * The demo has a new viewport and resolution, along with new sprites.

### Removed

  * `scripts/bootstrap`, replaced by `scripts/install`.  See above for details.
  * The requirements for Travis-CI no longer include `requirements/python2.txt` as they are no longer necessary.
  * Outdated references to PygAnimation.
  * The old anchor system, replaced in the module for animating sprites.

## [0.3.3] - 2015-11-01

### Added

  * More detailed platform-specific pygame install instructions in `README.md`

## [0.3.2] - 2015-11-01

Lily Lemmer

### Fixed

  * PyPi package description

### Added

  * `requirements/distrib.txt` for installing dependencies for `distrib.sh`
  * `etc/EXAMPLE-PYPIRC` to be copied to `~/.pypirc` and edited if you want to distribute/use `distrib.sh`

### Changed

  * `setup.py` uses the `setuptools-markdown` package to use `README.md` as the package description, which is much more reliable than the old `distrib.sh`
  * `distrib.sh` has one argument which must be either: _test_ or _live_. If the arg is _test_, it will distribute to the PyPi test site, otherwise, if the arg is __live__ it will publish to the main PyPi website.
  * `CONTRIBUTING.md` to mention `distrib.txt` and why you would use it.

## [0.3.1] - 2015-11-01

Lily Lemmer

### Added

  * `setup.cfg` file used to specify the package description as `README.md` for PyPi distributing (see: `distrib.sh`).

### Changed

  * `AnimatedSprite.total_duration()` renamed to `AnimatedSprite.get_total_duration()`

### Fixed

  * `AnimatedSprite.total_duration()` renamed to `AnimatedSprite.get_total_duration()`, because there is an attribute of the same name, i.e., `AnimatedSprite.total_duration`.

### Removed

  * Lines from `distrib.sh` which converts `README.md` for the package description for PyPi distributing.

## [0.3.0] - 2015-10-31

Halloween release! "Oops, I waited too long to release" edition!

Please forgive me if I missed anything or err, there's just *so many* changes.

Lily Lemmer

### Added

  * Python 3.5 support
  * Platform-specific pre-requisite instructions in `README.md`
  * Anchor maths, type-checking
  * Base class for all TMX-related exceptions
  * Windows test script
  * animatedsprite module: AnimatedSprite class replaces pyganim
  * New demo sprites, tilemap, settings
  * Add `all()` method to Action enum, which returns all available actions
  * Add `cardinals_and_ordinals()` static method to Direction
  * Add Scene.render()
  * Allow loading of resources from an unpacked directory.
  * Create new Direction method, disposition
  * tests
  * more comments!
  * better docstrings

### Changed

  * `README.md`
  * Revamped `CONTRIBUTING.md`
  * Replace AnimatedSprite.current_frame() with a property of the same function; AnimatedSprite.current_frame is updated with the current frame every time AnimatedSprite.update() is called.
  * Update `AUTHORS.md`
  * tests
  * Change debug walkabout
  * Change game/demo's viewport dimensions
  * Change debug TMX scene
  * Rename LabeledSurfaceAnchors to FrameAnchors
  * FrameAnchors.__init__() now only takes a dictionary. To load with config see new method FrameAnchors.from_config(). Reflecting changes where required. 
  * Rename AnimatedSpriteFrame to Frame
  * Changed dialogbox font size
  * Modify Walkabout to inherit pygame.sprite.Sprite. Add image attribute; set by the update method. Blit method split into and uses update method.

### Fixed

  * `test.sh` uses the `$PAGER` environmental variable instead of `more`
  * `test.sh` allows for different python versions
  * `README.md` repo install instructions
  * Anchor math
  * Docstrings
  * `.gitignore` PKG-INFO
  * Bug #80: python 3 unicode issues when reading files in resources.py. Resource files read as binary/rb
  * Fix/implement support for Walkabouts which use ONE sprite for ALL action/direction combinations (only)
  * Fix Walkabout `update()` method so Walkabout's `image` attribute is set to the active animation image, thereafter updating said active animation
  * tests
  * Resolved bug in Direction.from_velocity(): it previously only worked for generating ordinal products whereas there are nonzero values for both axis. This allows for NO direction as well as cardinal directions. Now when a velocity is (0, 0) the returned direction is None.

### Removed

  * pyganim as dependency
  * Anchor.add_ints()
  * Remove "encoding" as an argument from AnimatedSprite.pil_image_to_pygame_surface()
  * Remove `hat` walkabout 

## [0.2.29] - 2015-07-23

### Changed

  * README.md syntax error for PyPI

## [0.2.28] - 2015-07-23

### Changed

  * I put the directory and file notes from `README.md` to `CONTRIBUTING.md`. I did this because the directory and file notes don't pertain to the PyPi page.

## [0.2.27] - 2015-07-23

You can now use tiled editor to edit/create scenes. Things are still kinda a mess from just implementing this feature. There may be some bugs I'm not aware of. I rushed this out-the-door. The next update will probably be a cleanup.

### Added

  * Support for assembling a `Scene` from a Tiled map editor TMX file. See: `Scene.from_tmx_resource()`.
  * `objectproperties.xml` for tiled map editor
  * a lot more comments for clarity!
  * A new contributor: William D. Jones
  * Exceptions related to TMX data
  * Example TMX/Tiled editor map for showing off the new TMX support
  * `Scene.create_human_player()` static method
  * "AbsolutePosition" scaffolding in physics
  * More scaffolding to sound
  * various script notes
  * `Scene.from_resource()` class method
  * `Scene.from_tmx_resource()` class method
  * `TMX` object to represent supported data from a TMX file.
  * `install-netbsd-python2.sh` for installing on NetBSD. Thanks William D. Jones!
  * Instructions for the files and directories of the Hypatia project in `README.md`
  * `README.md` for scene resource directory
  * Example debugging tileset `tilesheet-for-tmx-example.png` especially for editing the TMX/Tiled map (Tiled will crash without it)
  * Static method for scenes to create a human player.

### Changed

  * Walkabouts should hopefully be optional for npcs, actors now
  * Code cleanup
  * `AUTHORS.md`, just changing the "a big thanks" section and my bit, plus
    adding William D. Jones as a contributor.
  * `CONTRIBUTING.md` is more thorough
  * Demo loads scene from TMX, a newly constructed scene
  * Default scene constructor only takes its attributes as arguments.
  * Game constructor takes a scene object, not a scene name.
  * `demo/game.py` reflects new construction argument for scene
  * Docstrings are be better
  * Actor.say() will return True if it has something to say, False if not.

## [0.2.26] - 2015-07-16

### Added

  * `controllers.py` module-level docstring which elaborates on the module. General docstring updates in this module.
  * `controllers.MenuController` scaffolding

### Fixed

  * decreased cyclomatic complexity in `controllers.WorldController.handle_input()`.

### Changed

  * `AUTHORS.md` file updated to include more info, including emails, and includes our new community managers!
  * Icon xfc and png files in `media/icons`

## [0.2.25] - 2015-07-14

### Added

  * coverage/tests for actor, constants, and physics modules
  * `controllers` module, related to human input control for controlling stuff in the game
  * `constants.Direction.cardinal()` class method returns the cardinal directions: north, east, south, and west.
  * `constants.Direction.x_plus()` class method associated with the moving x+
  * `constants.Direction.x_minus()` class method associated with the moving x-
  * `constants.Direction.y_plus()` class method associated with the moving y+
  * `constants.Direction.y_minus()` class method associated with the moving y-
  * `constants.Direction.from_velocity()` class method which returns the direction infered from velocity

### Changed

  * `game` module changed a lot--moved move player to humanplayer and handle input to the controllers module
  * reordered walk, stand enums in `constants.Action`
  * Improved `AUTHORS.md` file.
  * `distrib.sh` now checks validity of rst generated by pandoc.
  * `actor.Actor` uses `physics.Velocity` as a keyword argument and attribute
  * `actor.Actor` now has the `say()` and `talk()` methods (moved from players)
  * moved `game` module's collide check to `Scene` class

### Fixed

  * Removed duplicate `palette_cycle()` function in the animations module.
  * made actor use velocity, made the instance of human player start with a default velocity of 20

### Removed

  * The following attributes were removed from `constants.Direction`: x, y, cardinal. See: the addition of new Direction class methods in this update.
  * The doctest code (for testing the module) at the bottom of some hypatia modules

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
