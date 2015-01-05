# engine/entities.py
# Lillian Lynn Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Untitled Game Engine and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""Entities: interactive/dynamic map objects.

Interactive/stateful map stuff.

"""

import os
import glob
import render
import constants
import pyganim
import pygame
from collections import OrderedDict

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2014, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


class Walkabout(object):
    """Needs to use internal current_image pointer instead
    of relying on function. Then, you'll always test
    current_image.get_rect(), for example. This enables support
    for walkabout sprites of inconsistent dimensions.

    """

    def __init__(self, walkabout_directory='debug', start_position=None):
        """Graphical object with directional sprites and their
        movement/positioning/ollision detection.

        Note:
          The walkabout sprites specified to be therein
          walkabout_directory, are files with an action__direction.gif
          filename convention.

          ASSUMPTION: walkabout_directory contains sprites for
          walk AND run actions.

        Args:
          walkabout_directory (str): directory containing (animated)
            walkabout GIFs. Assumed parent is data/walkabouts/
          start_position (tuple): (x, y) coordinates (integers)
            referring to absolute pixel coordinate.

        Unfinished:
          * Anchors: head, hands, feet, torso

        """

        walkabout_directory = os.path.join(
                                           '../resources',
                                           'walkabouts',
                                           walkabout_directory
                                          )
        sprite_name_pattern = os.path.join(walkabout_directory, '*.gif')
        self.sprites = {}
        self.size = None

        # need to do test if none detected
        for sprite_path in glob.iglob(sprite_name_pattern):
            file_name, file_ext = os.path.splitext(sprite_path)
            file_name = os.path.split(file_name)[1]
            action, direction = file_name.split('_', 1)
            direction = getattr(constants, direction.title())
            animation = render.gif_to_pyganim(sprite_path)
            animation.convert()
            self.size = animation.getMaxSize()

            try:
                self.sprites[action][direction] = animation
            except KeyError:
                self.sprites[action] = {direction: animation}

        self.action = 'stand'
        self.direction = constants.Up
        self.speed = 1

        position = start_position or (0, 0)  # px values
        self.rect = pygame.Rect(position, self.size)

    # NOT TESTED
    @property
    def current_sprite(self):

        return self.sprites[self.action][self.direction]

    def blit(self, screen, offset):
        """Draw the appropriate/active animation to screen.

        Note:
          Should go to render module?

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
        self.current_sprite.blit(screen, position_on_screen)

        return None


class HumanPlayer(Walkabout):
    """Manipulation of walkabout specific to the human player.

    """

    def move(self, direction, tilemap):
        """Modify positional data to reflect a legitimate player
        movement operation.

        Note:
          Will round down to nearest probable step
          if full step is impassable.

        Args:
          direction (constants.Direction): may be one of: up, right, down, left
          tilemap (tiles.TileMap): tilemap for reference, so we can
            avoid walking into water and such.

        """

        self.direction = direction
        planned_movement_in_pixels = self.speed

        for pixels in xrange(planned_movement_in_pixels, 0, -1):
            new_topleft_x, new_topleft_y = self.rect.topleft

            if direction == constants.Up:
                new_topleft_y -= pixels
            elif direction == constants.Right:
                new_topleft_x += pixels
            elif direction == constants.Down:
                new_topleft_y += pixels
            elif direction == constants.Left:
                new_topleft_x -= pixels

            new_bottomright_x = new_topleft_x + self.size[0]
            new_bottomright_y = new_topleft_y + self.size[1]

            movement_size_x = abs(new_bottomright_x - self.rect.topleft[0])
            movement_size_y = abs(new_bottomright_y - self.rect.topleft[1])
            movement_area_size = (movement_size_x, movement_size_y)

            if direction == constants.Up:
                new_topleft = (new_topleft_x, new_topleft_y)
            elif direction == constants.Right:
                new_topleft = self.rect.topleft
            elif direction == constants.Down:
                new_topleft = self.rect.topleft
            elif direction == constants.Left:
                new_topleft = (new_topleft_x, new_topleft_y)

            movement_rectangle = pygame.Rect(new_topleft,
                                             movement_area_size)
            movement_rectangle_collides = False

            for impassable_area in tilemap.impassability:

                if impassable_area and (impassable_area
                                        .colliderect(movement_rectangle)):
                    movement_rectangle_collides = True
                    break

            if movement_rectangle_collides:
                # done; can't move!

                return False

            else:
                # we're done, we can move!
                new_topleft = (new_topleft_x, new_topleft_y)
                new_sprite_rect = pygame.Rect(new_topleft, self.size)

                self.rect = new_sprite_rect
                self.action = 'walk'

                return True


class Item(object):
    """An item on the ground which can be picked up.

    Note:
      An equipable item which has a sprite per side just
      uses Walkabout.

    """

    def __init__(self, position, item_name='debug'):
        item_image_path = os.path.join(
                                       '../resources',
                                       'items',
                                       item_name + '.png'
                                      )
        item_image = pygame.image.load(item_image_path)
        self.size = item_image.get_size()
        self.image = item_image
        self.rect = pygame.Rect(position, self.size)
        self.position = position
        sound_path = os.path.join(
                                  '../resources',
                                  'sounds',
                                  'touch-fuzzy.wav'
                                 )
        self.pickup_sound =  pygame.mixer.Sound(sound_path)

    def blit(self, surface):
        surface.blit(self.image, self.position)


class ExampleItem(Item):
    """Plays a sound and cycles the screen tint for a duration.

    """

    def pickup(self):
        self.pickup_sound.play()

