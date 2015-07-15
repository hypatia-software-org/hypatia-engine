# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""py.test unit testing for hypatia/constants.py

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


def test_direction():
    """Test constants.Direction class.

    """

    assert (constants.Direction.north + constants.Direction.west ==
            constants.Direction.north_west)

    assert (constants.Direction.north + constants.Direction.east ==
            constants.Direction.north_east)

    assert (constants.Direction.south + constants.Direction.west ==
            constants.Direction.south_west)

    assert (constants.Direction.south + constants.Direction.east ==
            constants.Direction.south_east)

    velocity = physics.Velocity(-22, 55)
    assert (constants.Direction.from_velocity(velocity) ==
            constants.Direction.south_west)

    assert (
            constants.Direction.north,
            constants.Direction.east,
            constants.Direction.south,
            constants.Direction.west
           ) == constants.Direction.cardinal()

    assert constants.Direction.x_plus() == constants.Direction.east
    assert constants.Direction.x_minus() == constants.Direction.west
    assert constants.Direction.y_plus() == constants.Direction.south
    assert constants.Direction.y_minus() == constants.Direction.north


def test_action():
    """Test constants.Action.

    """

    assert constants.Action.stand == constants.Action(1)
    assert constants.Action.walk == constants.Action(2)
