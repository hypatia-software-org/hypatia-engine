# engine/controllers.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""Controllers manipulate entity state/attributes.

Game object/entity "controller." A controller could be a gamepad, or a
remote player's gamepad, or an AI's gamepad.

This is currently kinda messy because there's some scaffolding, and
a lot of features I'm not using yet. Right now this module is only
being used for the user/player controller.

"""

import sys
import pygame
import constants
from pygame.locals import *

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2015, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


class Controller(object):

    def __init__(self, entity, tilemap, actions=None):
        """Actions manipulate an entity's attributes/state.

        In the future there will be an event stack (array).

        Args:
          entity (entities.*): the entity whose state/attributes will
            be manipulated, as defined in actions.
          tilemap (tiles.TileMap): tilemap for referencing from
            action triggers.
          actions (function): maps input to actions (triggers), see:
            self.update() or WalkaboutActions()

        """

        self.entity = entity
        self.tilemap = tilemap
        self.actions = actions or WalkaboutActions(self)

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

        self.actions.stateful_triggers()

        return None


class Triggers(object):

    def __init__(self):
        pass


class WalkaboutActions(object):

    def __init__(self, controller):
        """The actions/triggers which correspond to input.

        Args:
          controller (Controller): controller these actions
            are assigned to.

        """

        self.controller = controller
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

    def stateful_triggers(self):
        """Actions which trigger if key is being pressed.

        Args:
          controller (Controller): the controller to which these
            triggers/actions are assigned.

        Returns:
          None

        """

        controller = self.controller
        walkabout = controller.entity

        # directional keys; movement; up, right, down, left
        if not any([self.up, self.right, self.down, self.left]):
            walkabout.action = 'stand'

            return None

        if self.up:
            walkabout.move(constants.Up, controller.tilemap)

        if self.right:
            walkabout.move(constants.Right, controller.tilemap)

        if self.down:
            walkabout.move(constants.Down, controller.tilemap)

        if self.left:
            walkabout.move(constants.Left, controller.tilemap)

        return None

