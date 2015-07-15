"""Physical attributes of things.

"""

import pygame

from hypatia import constants


class Velocity(object):
    """Eight-directional velocity."""

    def __init__(self, x=0, y=0):
        """Speed in pixels per second per axis. Values may be negative.

        Args:
          x (int|None): --
          y (int|None): --

        """

        self.x = x
        self.y = y


class Position(object):
    """The absolute position of an object."""

    def __init__(self, x, y, size):
        """Extrapolate position info from supplied info.

        Args:
          x (int|float): how many pixels from the left of the scene.
          y (int|float): how many pixels from the top of the scene.
          size (tuple): (x, y) pixel dimensions of object being
            represented.

        """

        self.rect = pygame.Rect((x, y), size)
        self.float = (float(x), float(y))
        self.int = (x, y)
