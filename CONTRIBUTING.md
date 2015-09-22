# Contributing to Hypatia

This document directs potential contributors to resources for contributing to Hypatia.

## Quick Info

  * branch from `develop`
  * use descriptive branch names
  * pull requests back to `develop`
  * use `test.sh` to test before you commit!
  * You'll probably want to `pip install --user requirements/testing.txt`

## Must Reads

Please read [the project guidelines](http://hypatia-engine.github.io/wiki/contributing.html). It's a far more comprehensive guide for contributing to Hypatia.

You are expected to treat your fellow humans with dignity and respect. Please read the [`CODE-OF-CONDUCT.md`](CODE-OF-CONDUCT.md).

Checkout [the project's `etc/` directory](etc/). It contains additional/optional tools to assist Hypatia developers. Firstly, @ejmr was kind enough to make a pre-push script for git, which will automagically test your commit before it gets pushed, and if it fails, it won't push. There's also an `objecttypes.xml` to help Tiled map editor users.

## File and Directory Notes

### IMPORTANT

These files are *IMPORTANT* and you should read them before getting started with Hypatia:

  * CHANGELOG.md
  * LICENSE
  * CONTRIBUTING.md
  * CODE-OF-CONDUCT.md
  * README.md

### Install Scripts

The following scripts are available for installing Hypatia on specific platfroms from the repo source in the form `platform-major python version.sh`:

  * `install-netbsd-python2.sh`
  * `install-ubuntu-python2.sh`
  * `install-linuxmint-python3.sh`
  * `install-linuxmint-python2.sh`
  * `install-freebsd-python2.sh`
  * `install-base-python2.sh`: this shouldn't be directly ran.

### distribute.sh

This script is used for distributing A NEW RELEASE to PyPi.

### demo/

This directory hosts `game.py`, which is a demo of Hypatia. It also hosts the demo's editable resources.

### docs/

Sphinx docs source. Use the custom `make-sphinx.sh` to build the sphinx documentation from the docstrings.

The *built* Sphinx docs are published to the official Hypatia website, at the following URI: http://lillian-lemmer.github.io/hypatia/api

### etc/

*OPTIONAL* configurations/configuration scripts, helper files, etc. Worth checking out! Has a `objecttypes.xml` for Tiled editor!

### hypatia/

The actual Python package source.

### media/

Media, namely pictures, officially related to Hypatia as a project, e.g., logos, icons.

### requirements/

The requirements files installable by `pip`. Notes on the files:

|Requirements File|You'd want to use if...                        |
|-----------------|-----------------------------------------------|
|base.txt         |ALWAYS!                                        |
|python2.txt      |You use Python 2.x!                            |
|testing.txt      |You want to test and/or contribute to the code!|
|travis.txt       |NEVER                                          |

### tests/

Unit tests for py.test and Travis Continuous Integration. These files are for assuring Hypatia's API remains consistent, reproducible, functional, etc. They are in part what determines build success/fail according to Travis CI. See our `build` badge.

See also: `test.sh`, it's the official script to run when testing any changes.
