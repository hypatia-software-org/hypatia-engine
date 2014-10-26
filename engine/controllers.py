# engine/entities.py
# Lillian Lynn Mahoney <lillian.lynn.mahoney@gmail.com>
#
# This module is part of Untitled Game Engine and is released under the
# Attribution Assurance License: http://opensource.org/licenses/AAL

"""Controllers manipulate entity state/attributes.

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
__version__ = "0.3.2"
__maintainer__ = "Lillian Mahoney"
__email__ = "lillian.lynn.mahoney@gmail.com"
__status__ = "Development"


class Controller(object):

    def __init__(self, entity, actions=None):
        """Actions manipulate an entity's attributes/state.

        In the future there will be an event stack (array).

        Args:
          entity (entities.*): the entity whose state/attributes will
            be manipulated, as defined in actions.
          actions (function): maps input to actions (triggers), see:
            self.update() or WalkaboutActions()

        """

        self.entity = entity
        self.actions = actions or WalkaboutActions()

    def update(self):
        """Trigger actions based on input (keydown, keyup, ispressed).

        Triggers/actions (defined in self.actions) execute in the order:
          1. keydown_triggers(key)
          2. keyup_triggers(key)
          3. stateful_triggers(self)

        Please read about WalkaboutActions.

        Returns:
          None

        """

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                key = self.actions.key_to_label.get(event.key, event.key)
                self.actions.keydown_triggers(key)

            if event.type == KEYUP:
                key = self.actions.key_to_label.get(event.key, event.key)
                self.actions.keyup_triggers(key)

        self.actions.stateful_triggers(self)

        return None


class Triggers(object):

    def __init__(self):
        pass


class WalkaboutActions(object):

    def __init__(self):
        """The actions/triggers which correspond to input.

        """

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
        """Actions which trigger on keydown.

        Args:
          key (str): label corresponding to value in
            self.key_to_label.

        Returns:
          None

        """

        if key == 'escape':
            pygame.quit()
            sys.exit()

        if key in ('up', 'right', 'down', 'left'):
            setattr(self, key, True)

        return None

    def keyup_triggers(self, key):
        """Actions which trigger on keyup.

        Args:
          key (str): label corresponding to value in
            self.key_to_label.

        Returns:
          None

        """

        if key in ('up', 'right', 'down', 'left'):
            setattr(self, key, False)

        return None

    def stateful_triggers(self, controller):
        """Actions which trigger if key is being pressed.

        Args:
          controller (Controller): the controller to which these
            triggers/actions are assigned.

        Returns:
          None

        """

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

