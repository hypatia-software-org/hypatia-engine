# engine/gameblueprint.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia Engine and is released under the
# MIT License: http://opensource.org/licenses/MIT

"""Logic flow for the game.

Note:
  I have not decided firmly on the approach to take. Expect heavy
  changes in the future.

  Sorry for the poor documentation, I have not devised an actual
  architecture for this particular module. I have not decided
  firmly on the approach to take. Here, I'm sort of imitating
  Flask's app.

  Rename to "game.py".

"""

import pygame

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2015, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


class Game(object):
    """One simple object for referencing all of the game's features.

    """

    def __init__(self, screen, tilemap, viewport, human_player, items=None):
        self.human_player = human_player
        self.tilemap = tilemap
        self.viewport = viewport
        self.items = items or []
        self.screen = screen

    def init(self):
        self.tilemap.convert_layer_images()
        self.human_player.init()

    def item_check(self):
        ungot_items = []

        for item in self.items:

            if item.rect.colliderect(self.human_player.rect):
                # should this be player.pickup item? or both?
                item.pickup(self.human_player)
            else:
                ungot_items.append(item)

        self.items = ungot_items

    def blit_all(self):
        self.viewport.pan_for_entity(self.human_player)
        self.viewport.blit(self.tilemap.layer_images[0])

        for item in self.items:
            item.blit(self.viewport.surface,
                      (self.viewport.start_x, self.viewport.start_y))

        self.human_player.blit(
                               self.viewport.surface,
                               (
                                self.viewport.start_x,
                                self.viewport.start_y
                               )
                              )

        for layer in self.tilemap.layer_images[1:]:
            self.viewport.blit(layer)

