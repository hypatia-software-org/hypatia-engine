#!/bin/sh
#
# How I test before making a commit.

py.test tests --pep8 --doctest-modules hypatia -v --cov-report term-missing --cov=hypatia
