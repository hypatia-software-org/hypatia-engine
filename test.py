import pygame
from engine import tiles
from engine import entities
from engine import render


FILENAME = 'debug.tilemap'
LAYERS = 1
ROWS = 10
WIDTH = 10

# ENGINE: tiles
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

tilemap = tiles.TileMap('debug', blueprint)
tilemap_string = tilemap.to_string()

with open(FILENAME, 'w') as f:
    f.write(tilemap_string)

with open(FILENAME) as f:
    tilemap = tiles.tilemap_from_string(f.read())

render.render(tilemap)

