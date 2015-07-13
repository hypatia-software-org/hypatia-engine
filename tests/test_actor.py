# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""py.test unit testing for hypatia/actor.py

Run py.test on this module to assert hypatia.actor
is completely functional.

"""

import os

import pygame
import pytest

from hypatia import actor
from hypatia import physics
from hypatia import constants
from hypatia import animations

try:
    os.chdir('demo')
except OSError:
    pass


def test_actor():
    """Test actor.Actor class.

    """

    walkabout = animations.Walkabout('debug')
    velocity = physics.Velocity(10, 10)
    an_actor = actor.Actor(walkabout=walkabout,
                           say_text='Hello, world!',
                           velocity=velocity)
