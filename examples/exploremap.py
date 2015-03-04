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
screen = render.Screen()
game = Game(screen)

# set game font
game.font = pygame.font.Font('../resources/fonts/VeraMono.ttf', 11)

# set game viewport
game.viewport = render.Viewport((VIEWPORT_X, VIEWPORT_Y))

# set human player
hat = sprites.Walkabout('hat')
human_walkabout = sprites.Walkabout(children=[hat])
game.human_player = player.Player(walkabout=human_walkabout)

# set game tilemap
blueprint_string = """\
` grass
@ cobblestone_wall_top
= cobblestone_wall_upper
# cobblestone_wall
~ water

`~~~~~~~~~~~~~~~~
``````````````~~~
~```````````````~
~```````````````~
~```````````````~
~``@@@@@@@@@@@``~
~``@=========@``~
~``@#########@``~
~``@`````````@``~
~``=`````````=``~
~``#`````````#``~
~```````````````~
~``@@@@@@@@@@@``~
~~`===========``~
~~~###########`~~
~~~~~~~~~~~~~~~~~"""

blueprint = tiles.blueprint_from_string(blueprint_string)
game.tilemap = tiles.TileMap('debug', blueprint)

# ... and set tilemap npcs
npc_walkabout = sprites.Walkabout(position=(40, 40))
npc = player.Npc(walkabout=npc_walkabout, say_text="Hello! How're you?")
game.tilemap.npcs = [npc]

# finished!
game.start_loop()
