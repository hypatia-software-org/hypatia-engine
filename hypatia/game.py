# This module is part of Hypatia and is released under the
# MIT License: http://opensource.org/licenses/MIT

"""Why stuff is drawn; logic flow for the game.

Game logic, game component interaction.

Glues various modules/game components together with behaviors defined
in methods belonging to Game().

Note:
  I have not decided firmly on the approach to take. Expect heavy
  changes in the future.

  Sorry for the poor documentation, I have not devised an actual
  architecture for this particular module. I have not decided
  firmly on the approach to take. Here, I'm sort of imitating
  Flask's app.

"""

import os
import sys

try:
    import ConfigParser as configparser

except ImportError:
    import configparser

import pygame

from hypatia import util
from hypatia import tiles
from hypatia import dialog
from hypatia import render
from hypatia import player
from hypatia import physics
from hypatia import constants
from hypatia import animations
from hypatia import controllers


class Hypatia(object):

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)


class Game(object):
    """Simulates the interaction between game components."""

    def __init__(self, screen=None, scene_name=None,
                 viewport_size=None, dialogbox=None):

        self.screen = screen or render.Screen()
        self.viewport = render.Viewport(viewport_size)
        self.dialogbox = dialogbox or dialog.DialogBox(self.viewport.rect.size)

        # everything has been added, run runtime_setup() on each
        # relevant item
        self.scene = Scene(scene_name)
        self.scene.runtime_setup()
        self.start_loop()

    def render(self):
        """Drawing behavior for game objects.

        """

        first_tilemap_layer = self.scene.tilemap.layer_images[0]
        self.viewport.center_on(self.scene.human_player.walkabout,
                                first_tilemap_layer.get_rect())
        self.viewport.blit(first_tilemap_layer)
        self.scene.tilemap.blit_layer_animated_tiles(self.viewport, 0)

        # render each npc walkabout
        for npc in self.scene.npcs:
            npc.walkabout.blit(
                               self.viewport.surface,
                               self.viewport.rect.topleft
                              )

        # finally human and rest map layers last
        self.scene.human_player.walkabout.blit(
                                               self.viewport.surface,
                                               self.viewport.rect.topleft
                                              )

        for i, layer in enumerate(self.scene.tilemap.layer_images[1:], 1):
            self.viewport.blit(layer)
            self.scene.tilemap.blit_layer_animated_tiles(self.viewport, i)

        self.dialogbox.blit(self.viewport.surface)

    def start_loop(self):
        controller = controllers.WorldController(self)

        while controller.handle_input():
            controller.handle_input()
            self.screen.update(self.viewport.surface)
            self.render()

        pygame.quit()
        sys.exit()


class Scene(object):
    """A map with configuration data/meta, e.g., NPCs.

    Attributes:
      tilemap (hypatia.tiles.Tilemap): --
      player_start_position (tuple): (x, y); two integer tuple
        denoting the starting position for human player.
      human_player (hypatia.player.Player): the human player object.
      npcs (list): a list of hypatia.player.NPC objects

    """

    def __init__(self, scene_name):
        """

        Args:
          scene_name (str): the name of the directory which corresponds
            to the map you want to load from resources/maps.

        """

        # NEW IMPL
        resource = util.Resource('scenes', scene_name)
        scene_ini = resource['scene.ini']
        tilemap_string = resource['tilemap.txt']
        self.tilemap = tiles.TileMap.from_string(tilemap_string)

        # .. player start position
        player_start_x = scene_ini.getint('general', 'player_start_x')
        player_start_y = scene_ini.getint('general', 'player_start_y')
        self.player_start_position = (player_start_x, player_start_y)

        # .. create player with player scene data
        hat = animations.Walkabout('hat')
        start_position = self.player_start_position
        human_walkabout = animations.Walkabout('debug',
                                               position=start_position,
                                               children=[hat])
        velocity = physics.Velocity(20, 20)
        self.human_player = player.HumanPlayer(walkabout=human_walkabout,
                                               velocity=velocity)

        # npcs.ini
        npcs_ini = resource['npcs.ini']

        self.npcs = []

        for npc_name in npcs_ini.sections():
            walkabout_name = npcs_ini.get(npc_name, 'walkabout')
            position_x = npcs_ini.getint(npc_name, 'position_x')
            position_y = npcs_ini.getint(npc_name, 'position_y')
            position = (position_x, position_y)

            npc_walkabout = animations.Walkabout(walkabout_name,
                                                 position=position)

            if npcs_ini.has_option(npc_name, 'say'):
                say_text = npcs_ini.get(npc_name, 'say')
            else:
                say_text = None

            npc = player.Npc(walkabout=npc_walkabout, say_text=say_text)
            self.npcs.append(npc)

    def collide_check(self, rect):
        """Returns True if there are collisions with rect.

        """

        possible_collisions = self.tilemap.impassable_rects

        for npc in self.npcs:
            possible_collisions.append(npc.walkabout.rect)

        return rect.collidelist(possible_collisions) != -1

    def runtime_setup(self):
        """Initialize al the NPCs, tilemap, etc.

        """

        npcs_to_setup = tuple(npc.walkabout for npc in self.npcs)
        objects_to_setup = (self.tilemap, self.human_player.walkabout,)
        objects_to_setup = objects_to_setup + npcs_to_setup

        for object_to_setup in objects_to_setup + npcs_to_setup:
            object_to_setup.runtime_setup()
