"""Interactive map entities/players!

Note:
  Could even be something like a sign! Or the human player.

"""

from hypatia import constants
from hypatia import actor


class HumanPlayer(actor.Actor):

    def __init__(self, walkabout=None):
        super(HumanPlayer, self).__init__(walkabout)

    def talk(self, npcs, dialogbox):
        """Attempt to talk in current direction.

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


class Npc(actor.Actor):

    def __init__(self, *args, **kwargs):
        super(Npc, self).__init__(*args, **kwargs)
