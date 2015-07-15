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

    @classmethod
    def cardinal(cls):

        return (cls.north, cls.east, cls.south, cls.west)

    @classmethod
    def x_plus(cls):

        return cls.east

    @classmethod
    def x_minus(cls):

        return cls.west

    @classmethod
    def y_plus(cls):

        return cls.south

    @classmethod
    def y_minus(cls):

        return cls.north

    @classmethod
    def from_velocity(cls, velocity):
        """Return a direction which corresponds to the current 2D
        velocity.

        See Also:
            :class:`constants.Direction`

        Returns:
            :class:`constants.Direction`: --

        """

        collected_directions = []

        for axis in ['x', 'y']:
            plus_direction = getattr(Direction, axis + '_plus')()
            minus_direction = getattr(Direction, axis + '_minus')()
            axis_value = getattr(velocity, axis)

            if axis_value > 0:
                collected_directions.append(plus_direction)
            elif axis_value == 0:
                pass
            else:
                collected_directions.append(minus_direction)

        return collected_directions[0] + collected_directions[1]

    def __add__(cls, other_direction):
        """Combine one cardinal direction with another to get
        an ordinal direction.

        Args:
            other_direction (:class:`Direction`): --

        Returns:
            :class:`Direction`: an ordinal direction.

        Example:
          >>> Direction.east + Direction.north == Direction.north_east
          True

        """

        return Direction(cls.value + other_direction.value)


@enum.unique
class Action(enum.Enum):
    """Specific to movement of a sprite/surface.

    """

    stand = 1
    walk = 2
