# engine/render.py
# Lillian Lynn Mahoney <lillian.lynn.mahoney@gmail.com>
#
# This module is part of Untitled Game Engine and is released under the
# Attribution Assurance License: http://opensource.org/licenses/AAL

"""render.py: how stuff displays? it puts it all together.

Visual/aesthetically oriented code.

I need to make sure graphics are being converted
for efficiency at runtime...

This is currently hacked together.

Should have camera control.

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

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2014, Lillian Lemmer"
__credits__ = ["Lillian Mahoney"]
__license__ = "Attribution Assurance License"
__version__ = "0.8"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


# the viewport width/height in pixels
VIEWBOX_X = 50
VIEWBOX_Y = 50


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
    pygame.display.set_caption('Untitled Game')

    viewbox = pygame.Surface((VIEWBOX_X, VIEWBOX_Y))
    viewbox_start_x = 0
    viewbox_start_y = 0
    viewbox_end_x = VIEWBOX_X
    viewbox_end_y = VIEWBOX_Y

    tilemap = tiles.load_tilemap('debug')
    tilemap.layer_images.convert()
    tile_width, tile_height = tilemap.layer_images.tile_size

    player = entities.Player()
    player_controller = controllers.Controller(player, tilemap)

    while True:
        player_pos_x, player_pos_y = player.walkabout.rect.center

        # if player goes off the right of the screen...
        if player_pos_x > viewbox_end_x:
            viewbox_start_x += VIEWBOX_X
            viewbox_end_x += VIEWBOX_X

        # if player goes off the left of the screen...
        elif player_pos_x < viewbox_start_x:
            viewbox_start_x -= VIEWBOX_X
            viewbox_end_x -= VIEWBOX_X

        # if player goes off bottom of screen...
        elif player_pos_y > viewbox_end_y:
            viewbox_start_y += VIEWBOX_Y
            viewbox_end_y += VIEWBOX_Y

        # if player goes off top of screen...
        elif player_pos_y < viewbox_start_y:
            viewbox_start_y -= VIEWBOX_Y
            viewbox_end_y -= VIEWBOX_Y

        viewbox.blit(
                     tilemap.layer_images.images[0],
                     (0, 0),
                     (viewbox_start_x, viewbox_start_y,
                      VIEWBOX_X, VIEWBOX_Y)
                    )

        for layer in tilemap.layer_images.images[1:]:
            viewbox.blit(layer, (0, 0))

        player_controller.update()
        player.walkabout.blit(viewbox, (viewbox_start_x, viewbox_start_y))
        pygame.display.update()

        new = pygame.transform.scale(viewbox, screen_size)
        screen.blit(
                    new,
                    (0, 0)
                   )
        pygame.display.flip()
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


