# Contributing to Hypatia

This document directs potential contributors to resources for contributing to Hypatia.

## Quick Info

  * branch from `develop`
  * use descriptive branch names
  * pull requests back to `develop`
  * use `test.sh` to test before you commit!
  * You'll probably want to `pip install --user requirements/testing.txt`

## Must Reads

Please read [the project guidelines](https://github.com/lillian-lemmer/hypatia/wiki/Project-Guidelines). It's a far more comprehensive guide for contributing to Hypatia.

You are expected to treat your fellow humans with dignity and respect. Please read the [`CODE-OF-CONDUCT.md`](CODE-OF-CONDUCT.md).

Checkout [the project's `etc/` directory](etc/). It contains additional/optional tools to assist Hypatia developers. Firstly, @ejmr was kind enough to make a pre-push script for git, which will automagically test your commit before it gets pushed, and if it fails, it won't push. There's also an `objecttypes.xml` to help Tiled map editor users.
