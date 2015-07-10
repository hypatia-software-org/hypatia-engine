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


# Intentionally not using `enum.IntEnum` because there is no reason to
# compare values of `Direction` to integers.
@enum.unique
class Direction(enum.Enum):
    """Compass direction. Specific to movement of a sprite/surface.

    Inspired by Unix numerical permissions. Only ever combined with
    one other direction max.

    See Also:
        :class:`physics.Velocity`

    Note:
        I don't see a point in having a separate class for ordinal
        and cardinal classes.

    """

    # Cardinal Directions
    #
    # The values for these directions are the powers of two because
    # that avoids potential conflicts with ordinal directions.  The
    # values for ordinal directions are the addition of their cardinal
    # components, e.g. `north_east` has the value of `north` plus
    # `east`.  Defining the cardinal directions as powers of two
    # avoids a problem by which ordinal directions could end up with
    # same values which would make equality comparisons true for
    # directions which should never be equal.
    north = 1
    east = 2
    south = 4
    west = 8

    # Ordinal Directions
    north_east = 3
    north_west = 9
    south_east = 6
    south_west = 12

    # just for fun
    north_south = 5
    east_west = 10

    def __add__(cls, other_direction):
        """Combine one cardinal direction with another to get
        an ordinal direction.

        Args:
            other_direction (:class:`Direction`): --

        Returns:
            :class:`Direction`: an ordinal direction.

        >>> Direction.east + Direction.north == Direction.north_east
        True
        """

        return Direction(cls.value + other_direction.value)


@enum.unique
class Action(enum.Enum):
    """Specific to movement of a sprite/surface.

    """

    walk = 1
    stand = 2


# let's run doctests first
if __name__ == "__main__":
    import doctest
    doctest.testmod()
