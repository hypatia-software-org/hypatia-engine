# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""Implementation of actors.

Actors are the base of any entities (players) which may perform
actions, examples include:

  * human player
  * an enemy NPC
  * a friendly NPC
  * an invisible NPC which simply displays
    a message when "talked" to.

This module implements a basic :class:`Actor` class to serve as
the parent for any classes representing objects such as those
examples.

Any logic which can by shared by all "players" belongs in the class,
for example, the logic for moving around the game world. This approach
makes it possible to allow, for example, enemies and players to share
much of the same behavior and this can make it easier to give monsters
the same set of core abilities and logic as NPCs, etc.

When type-checking is necessary the :class:`Actor` class provides a
useful way to test for objects which support a bare-minimum of core,
shared actions. The class is also useful in role-playing games for
storing data that tends to be common between the Player, NPCs, enemies,
etalia, a common example being statistics like hit-points.

"""

from hypatia import animations
from hypatia import constants
from hypatia import physics


class Actor(object):
    """The base class for any entity which can perform actions.

    For example, most actors can move around the game world, so
    there are tools for setting the "direction" the actor is
    facing. Another example: most actors can say something, offer
    some dialog. These are the types of actions which are shared
    by all/most actors and therefore best implemented in this class,
    allowing it to be shared by as many players as possible, e.g.,
    human player, enemies.

    Note:
      It is typically not useful to directly instantiate :class:`Actor`
      objects but the implementation does not prevent this.

    Attributes:
        walkabout (animations.Walkabout): --
        direction (constants.Direction): --

    See Also:
        :mod:`actor`

    """

    def __init__(self, walkabout=None, say_text=None, velocity=None):
        """Constructs a new Actor.

        Args:
            walkabout (Optional[animations.Walkabout]): Optionally
                set a walkabout property, which will graphically
                represent the actor.
            say_text (Optional[str]): Optionally set the text which
                is displayed when this actor's :meth:`Actor.say()`
                is called.
            velocity (Optional[physics.Velocity]): --

        """

        self.walkabout = walkabout
        self.say_text = say_text
        self.velocity = velocity or physics.Velocity()

    @property
    def direction(self):
        """An instance of :class:`constants.Direction`

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
        """Set the direction this actor is facing.

        Args:
            new_direction (constants.Direction): The new direction
                for the actor to face.

        Raises:
            AttributeError: If the new value is not a valid object
                of the :class:`constants.Direction` class.

        """

        if not isinstance(new_direction, constants.Direction):

            raise AttributeError(("Direction must be a valid "
                                  "constants.Direction value"))

        else:
            self.walkabout.direction = new_direction

    @direction.deleter
    def direction(self):
        """You are not allowed to delete the direction of an Actor.

        Raises:
            TypeError: If one tries to delete this property

        """

        raise TypeError("Cannot delete the 'direction' of an Actor")

    def say(self, at_direction, dialogbox):
        """Change this actor's direction, and say this actor's
        say_text in the global dialog box.

        This method is typically called by another
        actor's :meth:`actor.Actor.talk()`.

        Args:
            at_direction (constants.Direction): The new direction
                for this actor to face.
            dialogbox (dialog.DialogBox): the DialogBox to print
                this actor's say_text to.

        Returns:
            bool: True if this actor can and did say something, False
                if this actor cannot say something. This quality is
                determined by the presence of say_text.

        Note:
            Even if this actor doesn't say anything, it will
            change the direction it's facing.

        """

        facing = {
                  constants.Direction.north: constants.Direction.south,
                  constants.Direction.east: constants.Direction.west,
                  constants.Direction.west: constants.Direction.east,
                  constants.Direction.south: constants.Direction.north
                 }[at_direction]
        self.walkabout.direction = facing

        if self.say_text:
            dialogbox.set_message(self.say_text)

            return True

        else:

            return False

    def talk(self, npcs, dialogbox):
        """Trigger another actor's :meth:`actor.Actor.say()` if
        they are immediately *in front* of this actor.

        See Also:

            * :attribute:`animations.Walkabout.direction`
            * :attribute:`Actor.direction`

        Args:
            npcs (List[player.Npc]): --
            dialogbox (dialog.DialogBox): --

        """

        # get the current direction, check a bit in front with a rect
        # to talk to npc if collide
        facing = self.walkabout.direction

        if facing is constants.Direction.north:
            disposition = (0, -1)
        elif facing is constants.Direction.east:
            disposition = (1, 0)
        elif facing is constants.Direction.south:
            disposition = (0, 1)
        elif facing is constants.Direction.west:
            disposition = (-1, 0)

        talk_rect = self.walkabout.rect.copy()
        talk_rect.move_ip(disposition)

        for npc in npcs:

            if npc.walkabout.rect.colliderect(talk_rect):
                npc.say(facing, dialogbox)
