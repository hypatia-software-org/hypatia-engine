import os
import sys
import collections

import pygame
from pygame.locals import *

sys.path.insert(0, '../engine')
import tiles
import sprites
import render
import player
from game import Game

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
VIEWPORT_X, VIEWPORT_Y = 256, 240


# NEW RUNTIME
viewport = render.Viewport((VIEWPORT_X, VIEWPORT_Y))
game = Game(viewport=viewport)

# set human player
hat = sprites.Walkabout('hat')
human_walkabout = sprites.Walkabout(children=[hat])
game.human_player = player.Player(walkabout=human_walkabout)

# set game tilemap
blueprint_string = """\
11 11 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13
13 11 11 11 11 12 13 13 11 11 11 11 13 13 13 13 13 13 11 11 11 11 11 13 13 13
13 11 11 11 11 11 11 64 11 11 11 11 11 11 13 13 13 11 11 11 11 11 11 13 13 13
13 11 64 11 11 11 11 11 11 12 11 11 65 11 13 11 11 11 11 11 64 11 11 11 13 13
13 11 11 65 11 64 11 11 11 11 11 11 11 11 11 11 64 11 11 11 11 11 11 11 11 13
13 13 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 12 11 11 11 11 13
13 13 11 12 11 03 00 00 00 00 00 00 03 64 11 12 11 11 11 11 11 11 11 11 11 13
13 11 11 11 11 01 08 08 08 55 08 08 01 11 11 11 11 11 11 11 11 11 11 11 11 13
13 11 11 11 11 01 08 08 08 08 08 08 01 11 11 11 11 11 11 11 11 65 11 11 13 13
13 64 11 11 11 01 08 08 08 08 08 08 01 11 65 11 11 11 64 11 11 11 11 11 13 13
13 13 11 11 11 01 08 08 08 08 08 08 01 11 11 11 11 11 11 11 11 11 11 11 11 13
13 13 11 11 65 01 08 08 08 08 08 08 01 11 11 11 11 11 11 11 11 11 11 11 11 13
13 13 11 11 11 02 08 00 00 08 00 02 02 11 11 11 12 11 11 11 11 11 11 11 11 13
13 12 11 11 11 11 11 11 11 64 11 11 11 11 11 11 11 11 11 64 11 11 11 11 11 13
13 11 11 64 11 11 11 11 11 11 11 11 11 65 11 11 11 11 11 11 11 11 11 11 11 13
13 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 12 11 13
13 13 11 11 11 11 11 11 12 11 11 11 11 11 11 64 11 11 11 11 11 64 11 11 11 13
13 13 13 13 11 11 11 11 11 11 11 13 13 13 13 11 11 11 11 11 11 11 11 11 13 13
13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13

-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 31 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 45 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 38 -1 -1 -1 -1 -1 -1 -1 -1 54 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 91 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 99 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 39 -1 -1 -1 -1 -1 -1 -1 47 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 48 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 38 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 38 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1"""
tilemap = tiles.TileMap.from_string(blueprint_string)
#new_tilemap_string = tilemap.to_string()
#game.tilemap = tiles.TileMap.from_string(new_tilemap_string)
#print(game.tilemap.to_string())
game.tilemap = tilemap

# ... and set tilemap npcs
npc_walkabout = sprites.Walkabout(position=(140, 140))
npc_say = """\
START Praesent a dignissim ipsum. Etiam venenatis purus est, ornare sollicitudin velit scelerisque eget. Ut consequat odio tortor, eu lobortis sem viverra in. Maecenas maximus nunc in consectetur tempor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Suspendisse a sapien interdum, venenatis erat eu, faucibus lorem. Quisque erat lacus, varius a lorem vitae, posuere molestie erat. In interdum, dolor et vestibulum placerat, lectus massa tempus purus, eget pharetra mauris sapien eget turpis. Curabitur nec eleifend quam, nec scelerisque leo. Fusce tempus sem ex, eu gravida tellus sagittis nec. Aenean cursus pretium urna, id congue metus rutrum quis. Cras at nisi ac nibh aliquam maximus quis at turpis. Morbi commodo id odio ac scelerisque. Nunc eros diam, faucibus et volutpat in, feugiat nec turpis. Suspendisse fermentum efficitur enim sit amet volutpat. END"""
npc = player.Npc(walkabout=npc_walkabout, say_text=npc_say)
game.tilemap.npcs = [npc]

# finished!
game.start_loop()
