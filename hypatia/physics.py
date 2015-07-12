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

    def get_direction(self):
        """Return a direction which corresponds to the current 2D
        velocity.

        See Also:
            :class:`constants.Direction`

        Returns:
            :class:`constants.Direction`: --

        """

        x_directions = ('x', constants.Direction.east,
                        constants.Direction.west)
        y_directions = ('y', constants.Direction.south,
                        constants.Direction.north)

        collected_directions = []

        for direction_info in [x_directions, y_directions]:
            axis, plus_direction, nevative_direction = direction_info
            axis_value = getattr(self, axis)

            if axis_value > 0:
                collected_directions.append(plus_direction)
            elif axis_value == 0:
                pass
            else:
                collected_directions.append(negative_direction)

        return sum(collected_directinos)


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


# NOTE: this module will definitely be heavy on the tests in the future
if __name__ == "__main__":
    import doctest
    doctest.testmod()
