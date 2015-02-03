import os
import sys
import collections

import pygame
from pygame.locals import *

sys.path.insert(0, '../engine')
import sprites
import tiles
import render
import game

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2015, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


FILENAME = 'debug.tilemap'
LAYERS = 2
ROWS = 10
WIDTH = 10
VIEWPORT_X, VIEWPORT_Y = 50, 50


# TILEMAP
blueprint = [[['default' for i in range(WIDTH)]
                         for i in range(ROWS)]
                         for i in range(LAYERS)]

# I'm drawing a border of water around the default tile, but I'm
# leaving two parts of the wall open so I can have fun with nodraw.
for z in range(LAYERS):

    for y in range(ROWS):

        for x in range(WIDTH):

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

with open(FILENAME, 'wb') as f:
    f.write(tilemap_string)

#with open(FILENAME, 'rb') as f:
#    tilemap = tiles.tilemap_from_string(f.read())

# init screen

# prepare game assets
items = [sprites.ExampleItem((40, 40))]
player = sprites.Walkabout()
viewport = render.Viewport((VIEWPORT_X, VIEWPORT_Y))

game_blueprint = game.Game(
                           tilemap=tilemap,
                           human_player=player,
                           items=items,
                           viewport=viewport
                          )

# runtime
game_blueprint.init()
first_time = True

while True:
    game_blueprint.item_check()
    game_blueprint.handle_input()
    #player_controller.update()

    game_blueprint.blit_all()
    game_blueprint.screen.update(viewport.surface)

