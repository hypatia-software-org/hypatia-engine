# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""py.test unit testing for hypatia.animations

Run py.test on this module to assert hypatia.animations
is completely functional.

Example:
  Use from project root like so:

  $ py.test tests

"""

import os

import pygame
import pytest

from hypatia import render

try:
    os.chdir('demo')
except OSError:
    pass
