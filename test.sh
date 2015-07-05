#!/bin/sh
#
# How I test before making a commit.

pip uninstall hypatia_engine -y
pip install --user --no-cache-dir .
py.test tests --pep8 --doctest-modules hypatia -v --cov-report term-missing --cov=hypatia | more
