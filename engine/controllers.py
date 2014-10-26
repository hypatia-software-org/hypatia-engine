# engine/entities.py
# Lillian Lynn Mahoney <lillian.lynn.mahoney@gmail.com>
#
# This module is part of Untitled Game Engine and is released under the
# Attribution Assurance License: http://opensource.org/licenses/AAL

"""controllers: entity gamepad/input/controller and AI.

Game object/entity "controller." A controller could be a gamepad, or a
remote player's gamepad, or an AI's gamepad.

"""

from pygame.locals import *
import pygame
import sys


__author__ = "Lillian Lynn Mahoney"
__copyright__ = "Copyright 2014, Lillian Lynn Mahoney"
__credits__ = ["Lillian Mahoney"]
__license__ = "Attribution Assurance License"
__version__ = "0.3.1"
__maintainer__ = "Lillian Mahoney"
__email__ = "lillian.lynn.mahoney@gmail.com"
__status__ = "Development"


class Controller(object):

    def __init__(self, entity, actions=None):
        """Actions manipulate an entity's attributes/state.

        In the future there will be an event stack (array).

        Args:
          entity (entities.*): the Player being controlled.
          actions (function): 

        """

        self.entity = entity
        self.actions = actions or WalkaboutActions()

    def update(self):

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                key = self.actions.key_to_label.get(event.key, event.key)
                self.actions.keydown_triggers(key)

            if event.type == KEYUP:
                key = self.actions.key_to_label.get(event.key, event.key)
                self.actions.keyup_triggers(key)

        self.actions.stateful_triggers(self)

        return None


class WalkaboutActions(object):

    def __init__(self):
        self.key_to_label = {
                             K_ESCAPE: 'escape',
                             K_UP: 'up',
                             K_RIGHT: 'right',
                             K_DOWN: 'down',
                             K_LEFT: 'left',
                            }

        for label in self.key_to_label.values():
            setattr(self, label, False)

    def keydown_triggers(self, key):

        if key == 'escape':
            pygame.quit()
            sys.exit()

        if key in ('up', 'right', 'down', 'left'):
            setattr(self, key, True)

        return None

    def keyup_triggers(self, key):

        if key in ('up', 'right', 'down', 'left'):
            setattr(self, key, False)

        return None

    def stateful_triggers(self, controller):
        walkabout = controller.entity.walkabout

        # directional keys; movement; up, right, down, left
        if not any([self.up, self.right, self.down, self.left]):
            walkabout.action = 'stand'

            return None

        if self.up:
            walkabout.move('up')

        if self.right:
            walkabout.move('right')

        if self.down:
            walkabout.move('down')

        if self.left:
            walkabout.move('left')

        return None

