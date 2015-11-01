#!/bin/sh

# Distribute on PyPI.
#
# Setup for zsh with FreeBSD with Python 2.

rm -rf build dist

# This section used to create the PKG-INFO file
# for PyPi. I've left it in just-in-case. It
# is no longer required because of the setup.cfg.
# 
#     pandoc README.md -t rst -o PKG-INFO
#
# this checks pypi rst validity
#
#     python setup.py check -r -s

python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf build dist PKG-INFO
rm -rf hypatia_engine.egg-info
