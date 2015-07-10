# This module is part of Hypatia and is released under the
# MIT License: http://opensource.org/licenses/MIT

"""Constants for Hypatia Engine

Right now this just contains stuff pertaining to Walkabout, i.e.,
direction and action specifications. These classes are to be passed as
parameters.

Examples:
  >>> from hypatia import animations
  >>> sprite = animations.Walkabout('debug')
  >>> sprite.animations[Action.walk][Direction.east]
  <pyganim.PygAnimation object at 0x...>

"""

import enum


# intentionally not using intenum
class Direction(enum.Enum):
    """Compass direction. Specific to movement of a sprite/surfac.

    Inspired by Unix numerical permissions. Only ever combined with
    one other direction max.

    See Also:
        :class:`physics.Velocity`

    Note:
        I don't  see a point in having a separate class for ordinal
        and cardinal classes.

    """

    # Cardinal directions
    north = 1
    east = 2
    south = 4
    west = 6

    # Ordinal directions
    north_east = 3
    noth_west = 7
    south_east = 6
    south_west = 10

    # just for fun
    north_south = 5
    east_west = 8

    def __add__(cls, other_direction):
        """Combine one cardinal direction with another to get
        an ordinal direction.

        Args:
            other_direction (:class:`Direction`): --

        Returns:
            :class:`Direction`: an ordinal direction.

        """

        # does this work
        return Direction(cls.value + other_direction.value)


class Action(enum.Enum):
    """Specific to movement of a sprite/surface.

    """

    walk = 1
    stand = 2


# let's run doctests first
if __name__ == "__main__":
    import doctest
    doctest.testmod()
