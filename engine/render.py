# engine/render.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia Engine and is released under the
# MIT License: http://opensource.org/licenses/MIT

"""How stuff is drawn; spite and surface manipulation.

Includes screen, viewport, and surface/animation manipulation.

Attributes:
  FPS (int): frames per second limit

"""

import sys
import time
import itertools
import collections

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


FPS = 60


class Screen(object):
    """Everything blits to screen!

    Notes:
      --

    Attributes:
      clock (pygame.time.Clock):
      time_elapsed_milliseconds (int): the time difference between
        the two most recent frames/updates in milliseconds.
      screen_size (tuple):
      screen (pygame.display surface): --

    """

    def __init__(self, filters=None):
        """Will init pygame.

        Args:
          filters (list): list of functions which takes and
            returns a surface.

        """

        pygame.init()
        self.clock = pygame.time.Clock()
        self.time_elapsed_milliseconds = 0
        display_info = pygame.display.Info()
        self.screen_size = (display_info.current_w, display_info.current_h)
        self.screen = pygame.display.set_mode(
                                              self.screen_size,
                                              FULLSCREEN | DOUBLEBUF
                                             )
        self.filters = filters

    def update(self, surface):
        """Update the screen; apply surface to screen, automatically
        rescaling for fullscreen.

        """
        
        scaled_surface = pygame.transform.scale(surface, self.screen_size)

        if self.filters:

            for filter_function in self.filters:
                scaled_surface = filter_function(scaled_surface)

        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        self.time_elapsed_milliseconds = self.clock.tick(FPS)


class Viewport(object):
    """Display only a fixed area of a surface.

    Attributes:
      surface
      rect

    """

    def __init__(self, size):
        """

        Args:
          size (tuple): (int x, int y) pixel dimensions of viewport.

        Example:
          >>> viewport = Viewport((320, 240))

        """

        self.surface = pygame.Surface(size)
        self.rect = pygame.Rect((0, 0), size)

    def center_on(self, entity):
        """Center the viewport rectangle on an object.
        
        Note:
          entity must have entity.rect (pygame.Rect)

        Args:
          entity: something with an attribute "rect" which value is
            a pygame.Rect.

        """

        entity_position_x, entity_position_y = entity.rect.center
        difference_x = entity_position_x - self.rect.centerx
        difference_y = entity_position_y - self.rect.centery
        self.rect.move_ip(*(difference_x, difference_y))

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
                          self.rect
                         )


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


def shift_palette(surface):
    """Cycle the palette of surface after generating an index for it.

    Args:
      surface (pygame.Surface): the surface you wish to shift the
        palette of.

    """

    surface = surface.convert(8)
    palette = collections.deque(surface.get_palette())
    palette.rotate(1)
    surface.set_palette(palette)

    return surface


