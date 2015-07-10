# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""Implementation of actors.

Actors are the base of any entities which may perform actions. Examples
of actors are enemies, NPCs, the player themselves, etc. This module
implements a basic :class:`Actor` class to serve as the parent for any
classes representing objects such those examples. Any logic which can
be shared by all objects belongs in the class, for example, the logic
for moving around the game world. This approach makes it possible to
allow, for example, enemimes and players to share much of the same
behavior, a nd this can be useful by making it easer (from a
programming point-of-view) to give monsters the same set of core
abilities and logic as NPCs, etc.

When type-checking is necessary the :class:`Actor` class provides a
useful way to test for objects which support a bare-minimum of core,
shared actions.  The class is also useful in role-playing games for
storing data that tends to be common between the Player, NPCs, enemies,
etalia, a common example being statistics like hit-points.

"""

from hypatia import animations
from hypatia import constants
from hypatia import physics


class Actor(object):
    """The base class for any entity which can perform actions.

    For example, both :class:`player.Player` and :class:`player.NPC`
    objects can move around the game world. This is the type of action
    which is shared by all "actors" and therefore best implemented in
    this class, allowing it to be shared by as many entities as
    possible, e.g. enemies.

    It is typically not useful to directly instantiate :class:`Actor`
    objects but the implementation does not prevent this.

    Attributes:
        walkabout (:class:`animations.Walkabout`): instance.

    """

    def __init__(self, walkabout, say_text=None):
        """Constructs a new Actor.

        Args:
            walkabout (:class:`animations.Walkabout`): Walkabout which
                is then accessible via the ``walkabout`` property. This
                argument is optional and defaults to new instance
                of :class:`animations.Walkabout`.

        """

        self.walkabout = walkabout or animations.Walkabout()
        self.say_text = say_text or None
        self.velocity = physics.Velocity(x=20, y=20)

        @property
        def direction(self):
            """An intsance of :class:`constants.Direction`

            This property indicates the direction the actor is facing.
            Is it possible to set this property to a new value.

            Raises:
                AttributeError: If the new value is not a valid object
                    of the :class:`constants.Direction` class.
                TypeError: If one tries to delete this property

            """
            return self.walkabout.direction

        @direction.setter
        def direction(self, new_direction):

            if not isinstance(new_direction, constants.Direction):

                raise AttributeError(("Direction must be a valid "
                                      "constants.Direction value"))

            else:
                self.walkabout.direction = new_direction

        @direction.deleter
        def direction(self):

            raise TypeError("Cannot delete the 'direction' of an Actor")

        def say(self, at_direction, dialogbox):
            facing = {
                      constants.Direction.Up: constants.Direction.Down,
                      constants.Direction.Right: constants.Direction.Left,
                      constants.Direction.Left: constants.Direction.Right,
                      constants.Direction.Down: constants.Direction.Up
                     }[at_direction]
            self.walkabout.direction = facing

            if self.say_text:
                dialogbox.set_message(self.say_text)
