# engine/entities.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Untitled Game Engine and is released under the
# Attribution Assurance License: http://opensource.org/licenses/AAL

"""Entities: interactive/dynamic map objects."""

import os
import glob
import render
import pyganim
import pygame
from collections import OrderedDict


__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2014, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "Attribution Assurance License"
__version__ = "0.5"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


class Player(object):

    def __init__(self, walkabout=None):
        """NPC or human player; depends on which controller
        is assigned.

        Args:
          walkabout (Walkabout): walkabout settings/sprites

        """

        self.walkabout = walkabout or Walkabout('debug')


class Walkabout(object):

    def __init__(self, walkabout_directory, start_position=None, speed=1):
        """Interactive entity which uses a walkabout sprite.

        An entity capable of walking about the map. Sprites for
        "walking about" are defined as action__direction.gif therein
        the specified walkabout_directory.

        ASSUMPTION: walkabout_directory contains sprites for
        walk, run actions.

        Args:
          walkabout_directory (str): directory containing (animated)
            walkabout GIFs. Assumed parent is data/walkabouts/
          start_position (tuple): (x, y) coordinates (integers)
            referring to absolute pixel coordinate.
          speed (int): the number of pixels moved per update/frame.
            Fraction of self.size; 1.0 is self.size,
            0.5 is self.size / 2.

        Unfinished:
          * Anchors: head, hands, feet, torso

        """

        walkabout_directory = os.path.join('data', 'walkabouts',
                                           walkabout_directory)
        sprite_name_pattern = os.path.join(walkabout_directory, '*.gif')
        self.sprites = {}
        self.size = None

        for sprite_path in glob.iglob(sprite_name_pattern):
            file_name, file_ext = os.path.splitext(sprite_path)
            file_name = os.path.split(file_name)[1]
            action, direction = file_name.split('_', 1)
            animation = render.gif_to_pyganim(sprite_path)
            animation.convert()
            self.size = animation.getMaxSize()

            try:
                self.sprites[action][direction] = animation
            except KeyError:
                self.sprites[action] = {direction: animation}

        self.action = 'stand'
        self.direction = 'up'
        self.speed = 3

        position = start_position or (0, 0)  # px values
        self.rect = pygame.Rect(position, self.size)

    def move(self, direction, tilemap, speed=None):
        """

        Will round down to nearest probable step if full step is impassable.

        Args:
          direction (str): may be one of: up, right, down, left
          tilemap (tiles.TileMap): tilemap for reference, so we can
            avoid walking into water and such.
          speed (int|None): pixels per second or inherent speed.

        """

        self.direction = direction
        planned_movement_in_pixels = speed or self.speed

        while True:
            x, y = self.rect.topleft
            new_position_impossible = False

            if direction == 'up':
                y -= planned_movement_in_pixels
            elif direction == 'right':
                x += planned_movement_in_pixels
            elif direction == 'down':
                y += planned_movement_in_pixels
            elif direction == 'left':
                x -= planned_movement_in_pixels

            new_position = (x, y)
            new_sprite_rect = pygame.Rect(new_position, self.size)

            # assure new position isn't on an impassable tile
            for impass_rect in tilemap.impassability:

                if impass_rect and impass_rect.colliderect(new_sprite_rect):
                    new_position_impossible = True

            if new_position_impossible:
                planned_movement_in_pixels -= 1
            else:

                break

        self.rect = new_sprite_rect
        self.action = 'walk'

        return True

    def blit(self, screen, offset):
        """Draw the appropriate/active animation to screen.

        Args:
          screen (pygame.Surface): the primary display/screen.
          offset (x, y tuple): the x, y coords of the absolute
            starting top left corner for the current screen/viewport
            position.

        Returns:
          None

        """

        x, y = self.rect.topleft
        x -= offset[0]
        y -= offset[1]
        position_on_screen = (x, y)
        self.sprites[self.action][self.direction].blit(
                                                       screen,
                                                       position_on_screen
                                                      )

        return None


def walkabout_generator():
    """Create the walkabout sprites for a character
    based off of some info.

    Gender, obvs.

    Why not make this a meta class?

    """

    pass

