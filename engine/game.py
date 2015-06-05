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
import dialog
import render

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2015, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


class Game(object):

    def __init__(self, screen=None, viewport=None, dialogbox=None):
        self.screen = screen or render.Screen()
        self.viewport = viewport or render.Viewport((256, 240))
        self.dialogbox = dialogbox or dialog.DialogBox(viewport.rect.size)
        
    def handle_input(self):
        """...

        Returns
          bool: returns True if escape was never pressed; returns
            false if escape pressed.

        """
        
        for event in pygame.event.get():

            if event.type == KEYUP:
                self.human_player.walkabout.action = constants.Stand
            
            # need to trap player in a next loop, release when no next
            if event.type == KEYDOWN and event.key == K_SPACE:

                # do until 
                if self.dialogbox.active:
                    self.dialogbox.next()
                else:
                    self.human_player.talk(self.tilemap.npcs, self.dialogbox)
        
        if self.dialogbox.active:
            
            return True
            
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_ESCAPE]:

            return False

        if pressed_keys[K_UP]:
            self.move_player(constants.Up)

        if pressed_keys[K_RIGHT]:
            self.move_player(constants.Right)

        if pressed_keys[K_DOWN]:
            self.move_player(constants.Down)

        if pressed_keys[K_LEFT]:
            self.move_player(constants.Left)

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

            if not self.collide_check(collision_rect):
                # we're done, we can move!
                new_topleft = (new_topleft_x, new_topleft_y)
                player.walkabout.action = constants.Walk
                animation = player.walkabout.current_animation()
                player.walkabout.size = animation.getMaxSize()
                player.walkabout.rect = destination_rect
                player.walkabout.topleft_float = new_topleft

                return True

        # never found an applicable destination
        player.walkabout.action = constants.Stand

        return False

    def collide_check(self, rect):
        """Returns True if there are collisions with rect.
        
        """
        
        possible_collisions = self.tilemap.impassable_rects
        
        for npc in self.tilemap.npcs:
            possible_collisions.append(npc.walkabout.rect)

        return rect.collidelist(possible_collisions) != -1

    def render(self):
        """Drawing behavior for game objects.

        """

        first_tilemap_layer = self.tilemap.layer_images[0]
        self.viewport.center_on(self.human_player.walkabout,
                                first_tilemap_layer.get_rect())
        self.viewport.blit(first_tilemap_layer)

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
            
        self.dialogbox.blit(self.viewport.surface)

    def start_loop(self):

        while self.handle_input():
            self.handle_input()
            self.screen.update(self.viewport.surface)
            self.render()

        pygame.quit()
        sys.exit()

