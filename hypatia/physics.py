"""Physical attributes of things.

"""

import pygame


class Velocity(object):
    """Eight-directional velocity."""

    def __init__(self, speed,
                 up=0, up_right=0, up_left=0,
                 left=0, right=0,
                 down=0, down_right=0, down_left=0):

        self.speed = speed

        self.up = up
        self.up_right = up_right
        self.up_left = up_left

        self.left = left
        self.right = right

        self.down = down
        self.down_right = down_right
        self.down_left = down_left


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

