#!/bin/sh

# Distribute on PyPI.
#
# Setup for zsh with FreeBSD with Python 2.

rm -rf build dist
pandoc README.md -t rst -o PKG-INFO
python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf build dist PKG-INFO
rm -rf hypatia_engine.egg-info
