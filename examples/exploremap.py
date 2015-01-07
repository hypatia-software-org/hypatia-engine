"""Render a map, simulate world.

Note:
  * Needs to be separate from simulation!
  * Mostly a basic test for development purposes.

"""

import os
import sys
sys.path.insert(0, '../engine')
import pygame
from pygame.locals import *
import entities
import tiles
import render
import controllers
import gameblueprint

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2014, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


FPS = 60
FILENAME = 'debug.tilemap'
LAYERS = 2
ROWS = 10
WIDTH = 10
VIEWPORT_X, VIEWPORT_Y = 50, 50


# TILEMAP
blueprint = [[['default' for i in xrange(WIDTH)]
                         for i in xrange(ROWS)]
                         for i in xrange(LAYERS)]

# I'm drawing a border of water around the default tile, but I'm
# leaving two parts of the wall open so I can have fun with nodraw.
for z in xrange(LAYERS):

    for y in xrange(ROWS):

        for x in xrange(WIDTH):

            if y == 0 and x > 0:
                blueprint[z][y][x] = 'water'
            elif y > 1 and x == 0:
                blueprint[z][y][x] = 'water'
            elif y > 1 and x == WIDTH - 1:
                blueprint[z][y][x] = 'water'
            elif y == ROWS - 1:
                blueprint[z][y][x] = 'water'

            if z > 0:
                blueprint[z][x][y] = 'air'

# showing off layer support with column
#         z  y  x
blueprint[0][2][2] = 'block-bottom'
blueprint[1][1][2] = 'block-top'

# write to file; load from file
tilemap = tiles.TileMap('debug', blueprint)
tilemap_string = tilemap.to_string()

with open(FILENAME, 'w') as f:
    f.write(tilemap_string)

with open(FILENAME) as f:
    tilemap = tiles.tilemap_from_string(f.read())

# init screen
pygame.init()
clock = pygame.time.Clock()
display_info = pygame.display.Info()
screen_size = (display_info.current_w, display_info.current_h)
screen = pygame.display.set_mode(
                                 screen_size,
                                 FULLSCREEN | DOUBLEBUF
                                )

# prepare game assets
items = [entities.ExampleItem((40, 40))]
player = entities.HumanPlayer()
player_controller = controllers.Controller(player, tilemap)
viewport = render.Viewport((VIEWPORT_X, VIEWPORT_Y))

game_blueprint = gameblueprint.GameBlueprint(
                                             tilemap=tilemap,
                                             human_player=player,
                                             items=items,
                                             screen=screen,
                                             viewport=viewport
                                            )

# runtime
game_blueprint.init()

while True:
    game_blueprint.item_check()
    player_controller.update()

    game_blueprint.blit_all()

    # this is such a nice way to rescale to any resolution
    scaled_viewport = pygame.transform.scale(
                                             viewport.surface,
                                             screen_size
                                            )
    screen.blit(
                scaled_viewport,
                (0, 0)
               )
    pygame.display.flip()
    clock.tick(FPS)

