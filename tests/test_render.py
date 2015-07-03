# tests/test_render.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""py.test unit testing for hypatia/render.py

Run py.test on this module to assert hypatia.render
is completely functional.

Example:
  Use from project root like so:

  $ py.test tests

"""

import os

import pygame
import pytest

from hypatia import render

# this script must be ran from project root
os.chdir("demo")

