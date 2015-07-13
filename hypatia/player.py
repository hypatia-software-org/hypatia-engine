"""Interactive map entities/players!

Note:
  Could even be something like a sign! Or the human player.

"""

from hypatia import constants
from hypatia import actor


class HumanPlayer(actor.Actor):

    def __init__(self, *args, **kwargs):
        actor.Actor.__init__(self, *args, **kwargs)


class Npc(actor.Actor):

    def __init__(self, *args, **kwargs):
        actor.Actor.__init__(self, *args, **kwargs)
