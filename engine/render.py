# engine/render.py
# Lillian Lynn Mahoney <lillian.lynn.mahoney@gmail.com>
#
# This module is part of Untitled Game Engine and is released under the
# Attribution Assurance License: http://opensource.org/licenses/AAL

"""render.py: how stuff displays? it puts it all together.

Visual/aesthetically oriented code.

Worst tagline, ever.

This is currently hacked together.

"""

from pygame.locals import *
from PIL import Image
import controllers
import entities
import pyganim
import pygame
import tiles
import time
import sys


__author__ = "Lillian Lynn Mahoney"
__copyright__ = "Copyright 2014, Lillian Lynn Mahoney"
__credits__ = ["Lillian Mahoney"]
__license__ = "Attribution Assurance License"
__version__ = "0.3"
__maintainer__ = "Lillian Mahoney"
__email__ = "lillian.lynn.mahoney@gmail.com"
__status__ = "Development"


def render(map_name):
    """IDK this is a test render job.

    Needs so much work. :/

    Args:
      map_name: map to render?

    Returns:
      None

    """

    pygame.init()
    fps = 30
    clock = pygame.time.Clock()
    display_info = pygame.display.Info()
    screen_size = (display_info.current_w, display_info.current_h)
    screen = pygame.display.set_mode(
                                     screen_size,
                                     FULLSCREEN | DOUBLEBUF
                                    )
    pygame.display.set_caption('Animation')

    player = entities.Player()
    sprite_x, sprite_y = player.walkabout.size
    screen_x, screen_y = screen_size
    new_player_size = (screen_x / sprite_x, screen_y / sprite_y)
    player.walkabout.resize(new_player_size)

    tilemap = tiles.load_tilemap('debug')
    tilemap.resize(screen_size)
    player_controller = controllers.Controller(player, tilemap)

    screen_x, screen_y = screen_size

    tile_width, tile_height = tilemap.layer_images.tile_size

    while True:
        screen.blit(tilemap.layer_images.images[0], (0, 0))
        player.walkabout.blit(screen)

        for layer in tilemap.layer_images.images[1:]:
            screen.blit(layer, (0, 0))

        player_controller.update()
        pygame.display.update()
        clock.tick(fps)

    return None


def gif_to_pyganim(gif_path):
    """Create PygAnimation from an animated GIF.

    Args:
      gif_path (str): path to GIF, used for creating PygAnimation

    Returns:
      PygAnimation: a PygAnimation based off of the GIF specified in
        gif_path

    """

    gif = Image.open(gif_path)
    frame_index = 0
    palette = gif.getpalette()
    frames = []  # (pygame.Surface, time in seconds [float])

    try:

        while 1:
            # must find frame time, create a pygame surface from frame
            gif.putpalette(palette)
            duration = gif.info['duration'] / 1000.0
            frame_as_pygame_image = pil_to_pygame(gif, "RGBA")
            frames.append((frame_as_pygame_image, duration))
            frame_index += 1
            gif.seek(gif.tell() + 1)

    except EOFError:
        pass # end of sequence

    animation = pyganim.PygAnimation(frames)
    animation.convert()
    animation.play()

    return animation


def pil_to_pygame(pil_image, encoding):
    """Convert PIL Image() to pygame Surface.

    Args:
      pil_image (Image): image to convert to pygame.Surface().
      encoding (str): image encoding, e.g., RGBA

    Returns:
      pygame.Surface: the converted image

    """

    image_as_string = pil_image.convert('RGBA').tostring()

    return pygame.image.fromstring(
                                   image_as_string,
                                   pil_image.size,
                                   'RGBA'
                                  )


