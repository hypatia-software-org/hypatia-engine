# This module is part of Hypatia and is released under the
# MIT License: http://opensource.org/licenses/MIT

"""Anything to do with game controls.

"""

import pygame
from pygame.locals import *

from hypatia import constants


class GameController(object):
    """Base input controller, "game pad," which is inherited
    by all input classes/controllers.

    """

    def __init__(self, game):
        self.game = game


class WorldController(GameController):
    """For the overworld."""

    def handle_input(self):
        """for overworld

        Returns
          bool: returns True if escape was never pressed; returns
            false if escape pressed.

        """

        for event in pygame.event.get():

            if event.type == KEYUP:
                (self.game.scene.human_player
                 .walkabout.action) = constants.Action.stand

            # need to trap player in a next loop, release when no next
            if event.type == KEYDOWN and event.key == K_SPACE:

                # do until
                if self.game.dialogbox.active:
                    self.game.dialogbox.next()
                else:
                    (self.game.scene.human_player
                     .talk(self.game.scene.npcs, self.game.dialogbox))

        if self.game.dialogbox.active:

            return True

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_ESCAPE]:

            return False

        if pressed_keys[K_UP]:
            self.game.scene.human_player.move(self.game,
                                              constants.Direction.north)

        if pressed_keys[K_RIGHT]:
            self.game.scene.human_player.move(self.game,
                                              constants.Direction.east)

        if pressed_keys[K_DOWN]:
            self.game.scene.human_player.move(self.game,
                                              constants.Direction.south)

        if pressed_keys[K_LEFT]:
            self.game.scene.human_player.move(self.game,
                                              constants.Direction.west)

        return True
