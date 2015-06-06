# engine/constants.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia Engine and is released under the
# MIT License: http://opensource.org/licenses/MIT

"""Constants for Hypatia Engine

Right now this just contains stuff pertaining to Walkabout, i.e.,
direction and action specifications. These classes are to be passed as
parameters.

Examples:
  >>> import sprites
  >>> sprite = sprites.Walkabout()
  >>> sprite.animations[Walk][Right]
  <Animation Object>

"""

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2015, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


class Direction(object):
    """Specific to movement of a sprite/surface."""
    pass


class Up(Direction):
    """Move in direction: up"""
    pass


class Right(Direction):
    """Move in direction: right"""
    pass


class Down(Direction):
    """Move in direction: down"""
    pass


class Left(Direction):
    """Move in direction: left"""
    pass


class Action(object):
    pass


class Walk(Action):
    pass


class Stand(Action):
    pass

