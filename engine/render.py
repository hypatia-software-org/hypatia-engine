# engine/render.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia Engine and is released under the
# MIT License: http://opensource.org/licenses/MIT

"""render.py: screen presentation and manipulation

Needs a lot of work. More of a demo/showcase right now.

Has some utils for managing images and animations.

"""

import sys
import time
import itertools

import pygame
import pyganim
from pygame.locals import *

import constants
import sprites
import tiles

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2015, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


class Viewport(object):
    """Display only a fixed area of a surface.

    Attributes:
      size (tuple): dimensions of viewport in pixels (int x, int y)
      surface (pygame.Surface): the "canvas" of the viewport, to which
        portions of other surfaces are blitted upon.
      start_x (int): the top-left corner x coordinate
      start_y (int): the top-left corner y coordinate
      end_x (int): the bottom-right corner x coorinate
      end_y (int): the bottom-right corner y coorindate

    """

    def __init__(self, size):
        """

        Args:
          size (tuple): (int x, int y) pixel dimensions of viewport.

        Example:
          >>> viewport = Viewport((320, 240))

        """

        self.size = size

        self.surface = pygame.Surface(size)
        self.start_x = 0
        self.start_y = 0
        self.end_x = size[0]
        self.end_y = size[1]

    def screen_pan(self, direction):
        """Move viewport in a given direction by one whole viewport
        in size.

        Args:
          direction (constants.Direction): Move the viewport toward
            specified direction.

        Example:
          >>> viewport.screen_pan(constants.Up)

        """

        if direction is constants.Right:
            self.start_x += self.size[0]
            self.end_x += self.size[0]

        # if player goes off the left of the screen...
        elif direction is constants.Left:
            self.start_x -= self.size[0]
            self.end_x -= self.size[0]

        # if player goes off bottom of screen...
        elif direction is constants.Down:
            self.start_y += self.size[1]
            self.end_y += self.size[1]

        # if player goes off top of screen...
        elif direction is constants.Up:
            self.start_y -= self.size[1]
            self.end_y -= self.size[1]

        else:
            # should raise InvalidDirection
            pass

    def pan_for_entity(self, entity):
        """Check if entity is outside of the viewport, and if so,
        in which direction?

        Args:
          entity (entity.Walkabout): something with a pygame.rect
            attribute. Uses rect.center for coordinates to check.

        Example:
          >>> tilemap_pan_for_entity(player)

        """

        entity_position_x, entity_position_y = entity.rect.center

        # if player goes off the right of the screen...
        if entity_position_x > self.end_x:
            self.screen_pan(constants.Right)

        # if player goes off the left of the screen...
        elif entity_position_x < self.start_x:
            self.screen_pan(constants.Left)

        # if player goes off bottom of screen...
        elif entity_position_y > self.end_y:
            self.screen_pan(constants.Down)

        # if player goes off top of screen...
        elif entity_position_y < self.start_y:
            self.screen_pan(constants.Up)

    def blit(self, surface):
        """Draw the correct portion of supplied surface onto viewport.

        Args:
          surface (pygame.Surface): will only draw the area described
            by viewport coordinates.

        Example:
          >>> viewport.blit(tilemap.layer_images[0])

        """

        self.surface.blit(
                          surface,
                          (0, 0),
                          (self.start_x, self.start_y,
                           self.size[0], self.size[1])
                         )


def anchor_to_animation(animation, animation_mask, pygame_image):
    """Afix a pygame image to the right point per frame in an
    animation. Merge surfaces at their anchors.

    Args:
      pygame_image (pygame.image): pygame.image.load('hat.png')
      alt_target (PygAnim): --

    Note:
      Precisely superimpose a surface by anchor onto each frame
      of an animation.

    Returns:
      pyganim.PygAnimation: --

    """

    gif_surfaces = animation.pygame_surfaces
    gif_mask_surfaces = animation_mask.pygame_surfaces

    gif_x, gif_y = gif_surfaces[0][0].get_size()
    pygame_image_anchor = find_anchors(pygame_image)
    pygame_image_anchor_x, pygame_image_anchor_y = pygame_image_anchor
    new_surfaces = []

    for i, frame in enumerate(gif_mask_surfaces):
        surface, duration = frame
        head_anchor = find_anchors(surface)

        if head_anchor:
            head_anchor_x, head_anchor_y = head_anchor
            new_x = head_anchor_x - pygame_image_anchor_x
            new_y = head_anchor_y - pygame_image_anchor_y
            new_topleft = (new_x, new_y)

            gif_surfaces[i][0].blit(pygame_image, new_topleft)

        else:

            raise Exception('this should be an UnfoundAnchor error')


    pyganim_gif = pyganim.PygAnimation(gif_surfaces)

    return sprites.Animation(pyganim_gif=pyganim_gif)


def pil_to_pygame(pil_image, encoding):
    """Convert PIL Image() to pygame Surface.

    Note:
      NOT for animations, use Animation() for that!

    Args:
      pil_image (Image): image to convert to pygame.Surface().
      encoding (str): image encoding, e.g., RGBA

    Returns:
      pygame.Surface: the converted image

    Example:
       >>> pil_to_pygame(gif, "RGBA")
       <pygame.Surface>

    """

    image_as_string = pil_image.convert('RGBA').tostring()

    return pygame.image.fromstring(
                                   image_as_string,
                                   pil_image.size,
                                   'RGBA'
                                  )


def find_anchors(surface):
    """Return the coordinates for specified anchors in surface.

    Note:
      An "anchor" is simply a pixel which matches a specified color.

      I created this for adding equipment to sprites.

    Returns:
      tuple|None: returns None if no anchors found on surface. Returns
        a tuple (int x, int y) corresponding to the location of the
        anchor/color on supplied surface.

    Examples:
      >>> find_anchors(some_character_sprite)
      (2, 4)

    """

    head_anchor_color = pygame.Color(255, 136, 255)
    x, y = surface.get_size()

    for coordinates in itertools.product(range(0, x), range(0, y)):
        color = surface.get_at(coordinates)

        if color == head_anchor_color:

            return coordinates

    return None


def cycle_palette(surface):
    scaled_viewport = scaled_viewport.convert(8)

    if first_time:
        palette = collections.deque(scaled_viewport.get_palette())
        first_time = False
    else:
        palette.rotate(1)
        scaled_viewport.set_palette(palette)


