# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""py.test unit testing for hypatia/physics.py

Run py.test on this module to assert hypatia.physics
is completely functional.

"""

import os

import pygame
import pytest

from hypatia import physics
from hypatia import constants

try:
    os.chdir('demo')
except OSError:
    pass


def test_velocity():
    """Test physics.Velocity class.

    """

    velocity = physics.Velocity(1, 2)
    assert velocity.x == 1 and velocity.y == 2

    velocity = physics.Velocity(x=1, y=2)
    assert velocity.x == 1 and velocity.y == 2

    velocity = physics.Velocity(-22, 55)
    assert (constants.Direction.from_velocity(velocity) ==
            constants.Direction.south_west)
