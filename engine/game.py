# engine/game.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia Engine and is released under the
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

import sys

import pygame
from pygame.locals import *

import constants
import render

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2015, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


class Game(object):

    def __init__(self, tilemap, viewport, human_player):
        self.human_player = human_player
        self.tilemap = tilemap
        self.viewport = viewport
        self.screen = render.Screen()

    def handle_input(self):
        """...

        Returns
          bool: returns True if escape was never pressed; returns
            false if escape pressed.

        """

        for event in pygame.event.get():

            if event.type == KEYUP:
                self.human_player.walkabout.action = constants.Stand

        keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]:

            return False

        if keys[K_UP]:
            self.move_player(constants.Up)

        if keys[K_RIGHT]:
            self.move_player(constants.Right)

        if keys[K_DOWN]:
            self.move_player(constants.Down)

        if keys[K_LEFT]:
            self.move_player(constants.Left)
        
        if keys[K_SPACE]:
            self.human_player.talk(self.tilemap.npcs)

        return True

    def move_player(self, direction):
        """Modify human player's positional data legally (check
        for collisions).

        Note:
          Will round down to nearest probable step
          if full step is impassable.
          
          Needs to use velocity instead...

        Args:
          direction (constants.Direction): may be one of: up, right, down, left
          tilemap (tiles.TileMap): tilemap for reference, so we can
            avoid walking into water and such.

        """

        player = self.human_player
        player.walkabout.direction = direction
        planned_movement_in_pixels = (player.walkabout.
                                      speed_in_pixels_per_second)
        adj_speed = self.screen.time_elapsed_milliseconds / 1000.0
        iter_pixels = max([1, int(planned_movement_in_pixels)])

        # test a series of positions
        for pixels in range(iter_pixels, 0, -1):
            # create a rectangle at the new position
            new_topleft_x, new_topleft_y = player.walkabout.topleft_float

            # what's going on here
            if pixels == 2:
                adj_speed = 1

            if direction == constants.Up:
                new_topleft_y -= pixels * adj_speed
            elif direction == constants.Right:
                new_topleft_x += pixels * adj_speed
            elif direction == constants.Down:
                new_topleft_y += pixels * adj_speed
            elif direction == constants.Left:
                new_topleft_x -= pixels * adj_speed

            destination_rect = pygame.Rect((new_topleft_x, new_topleft_y),
                                           self.human_player.walkabout.size)
            collision_rect = player.walkabout.rect.union(destination_rect)
            possible_collisions = self.tilemap.impassability
            
            for npc in self.tilemap.npcs:
                possible_collisions.append(npc.walkabout.rect)

            if not self.collide_check(collision_rect):
                # we're done, we can move!
                new_topleft = (new_topleft_x, new_topleft_y)
                player.walkabout.action = constants.Walk
                animation = player.walkabout.current_animation()
                player.walkabout.size = animation.get_max_size()
                player.walkabout.rect = destination_rect
                player.walkabout.topleft_float = new_topleft

                return True

        # never found an applicable destination
        player.walkabout.action = constants.Stand

        return False

    def collide_check(self, rect):
        """Returns True if there are collisions with rect.
        
        """
        
        possible_collisions = self.tilemap.impassability
        
        for npc in self.tilemap.npcs:
            possible_collisions.append(npc.walkabout.rect)

        return rect.collidelist(possible_collisions) != -1

    def render(self):
        """Drawing behavior for game objects.

        """

        self.viewport.center_on(self.human_player.walkabout)
        self.viewport.blit(self.tilemap.layer_images[0])

        # render each npc walkabout
        for npc in self.tilemap.npcs:
            npc.walkabout.blit(
                               self.viewport.surface,
                               self.viewport.rect.topleft
                              )

        # finally human and rest map layers last
        self.human_player.walkabout.blit(
                                         self.viewport.surface,
                                         self.viewport.rect.topleft
                                        )

        for layer in self.tilemap.layer_images[1:]:
            self.viewport.blit(layer)

    def start_loop(self):
        self.tilemap.convert_layer_images()
        self.human_player.walkabout.init()
        
        for npc in self.tilemap.npcs:
            npc.walkabout.init()

        while self.handle_input():
            self.handle_input()
            self.screen.update(self.viewport.surface)
            self.render()

        pygame.quit()
        sys.exit()

