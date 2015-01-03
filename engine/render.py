# engine/render.py
# Lillian Lynn Mahoney <lillian.lynn.mahoney@gmail.com>
#
# This module is part of Untitled Game Engine and is released under the
# Attribution Assurance License: http://opensource.org/licenses/AAL

"""render.py: screen presentation and manipulation

Needs a lot of work. More of a demo/showcase right now.

Has some utils for managing images and animations.

"""

import sys
import time
import tiles
import pygame
import pyganim
import entities
import controllers
from PIL import Image
from pygame.locals import *

__author__ = "Lillian Mahoney"
__copyright__ = "Copyright 2014, Lillian Mahoney"
__credits__ = ["Lillian Mahoney"]
__license__ = "Attribution Assurance License"
__maintainer__ = "Lillian Mahoney"
__email__ = "lillian.lynn.mahoney@gmail.com"
__status__ = "Development"


FPS = 30

# the viewport width/height in pixels
VIEWPORT_X = 50
VIEWPORT_Y = 50


def render(tilemap):
    """Render a map, simulate world.

    Needs to be separate from simulation!

    Mostly a basic test for development purposes.

    Args:
      tilemap (tiles.TileMap): tile map to render

    Returns:
      None

    """

    pygame.init()
    clock = pygame.time.Clock()
    display_info = pygame.display.Info()
    screen_size = (display_info.current_w, display_info.current_h)
    screen = pygame.display.set_mode(
                                     screen_size,
                                     FULLSCREEN | DOUBLEBUF
                                    )

    viewport = pygame.Surface((VIEWPORT_X, VIEWPORT_Y))
    viewport_start_x = 0
    viewport_start_y = 0
    viewport_end_x = VIEWPORT_X
    viewport_end_y = VIEWPORT_Y

    tilemap.convert_layer_images()

    player = entities.HumanPlayer()
    player_controller = controllers.Controller(player, tilemap)

    while True:
        player_pos_x, player_pos_y = player.walkabout.rect.center

        # if player goes off the right of the screen...
        if player_pos_x > viewport_end_x:
            viewport_start_x += VIEWPORT_X
            viewport_end_x += VIEWPORT_X

        # if player goes off the left of the screen...
        elif player_pos_x < viewport_start_x:
            viewport_start_x -= VIEWPORT_X
            viewport_end_x -= VIEWPORT_X

        # if player goes off bottom of screen...
        elif player_pos_y > viewport_end_y:
            viewport_start_y += VIEWPORT_Y
            viewport_end_y += VIEWPORT_Y

        # if player goes off top of screen...
        elif player_pos_y < viewport_start_y:
            viewport_start_y -= VIEWPORT_Y
            viewport_end_y -= VIEWPORT_Y

        viewport.blit(
                     tilemap.layer_images[0],
                     (0, 0),
                     (viewport_start_x, viewport_start_y,
                      VIEWPORT_X, VIEWPORT_Y)
                    )

        player_controller.update()
        player.walkabout.blit(viewport, (viewport_start_x, viewport_start_y))

        for layer in tilemap.layer_images[1:]:
            viewport.blit(
                          layer,
                          (0, 0),
                          (viewport_start_x, viewport_start_y,
                           VIEWPORT_X, VIEWPORT_Y)
                         )

        scaled_viewport = pygame.transform.scale(viewport, screen_size)
        screen.blit(
                    scaled_viewport,
                    (0, 0)
                   )
        pygame.display.flip()
        clock.tick(FPS)

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
    animation.anchor(pyganim.CENTER)
    animation.convert_alpha()
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


