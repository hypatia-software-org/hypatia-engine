"""Physical attributes of things.

Right now, not much differs it from the constants
module, but there will surely be much more to do
with physics as time progresses.

See Also:
    :mod:`constants`

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


# this really isn't used, yet
class Position(object):
    """The position of an object.

    Scaffolding.

    """

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


class AbsolutePosition(Position):
    """The absolute pixel coordinate in regard to the scene.

    Scaffolding.

    """

    pass
