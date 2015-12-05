#!/bin/sh

# Distribute a new release on PyPi.
#
# Test on the PyPi testing site before you distribute!
# https://testpypi.python.org/
#
# Prerequisites:
#     1. You'll need a PyPi Test Site account to proceed, which
#        you'll set in ~/.pyirc. The PyPi Test Site login is
#        separate from your regular PyPi login.
#     1. pip install -r requirements/distrib.sh
#     2. cp etc/EXAMPLE-PYPIRC ~/.pypirc
#     3. vim ~/.pypirc
#
# Usage:
#     ./distrib.sh TARGET_SITE
#
# Args:
#     TARGET_SITE -- either 'live' or 'test'. If test, distributes
#                    to the PyPi test repo. If live, distributes to
#                    PyPi. Otherwise an error!

rm -rf build dist  # ??

if [ "$1" = "live" ]; then
  python setup.py sdist bdist_wheel
  twine upload dist/*
elif [ "$1" = "test" ]; then
  python setup.py register -r pypitest
else
  exit 1
fi

rm -rf build dist PKG-INFO
rm -rf hypatia_engine.egg-info
