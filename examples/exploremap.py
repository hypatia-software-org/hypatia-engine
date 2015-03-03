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
import player

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
VIEWPORT_X, VIEWPORT_Y = 80, 80


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

# write to file; load from file
tilemap = tiles.TileMap('debug', blueprint)
tilemap_string = tilemap.to_string()

with open(FILENAME, 'wb') as f:
    f.write(tilemap_string)

with open(FILENAME, 'rb') as f:
    tilemap = tiles.tilemap_from_string(f.read())

# prepare game assets
hat = sprites.Walkabout('hat')
human_walkabout = sprites.Walkabout(children=[hat])
human = player.Player(walkabout=human_walkabout)

npc_walkabout = sprites.Walkabout(position=(40, 40))
npc = player.Npc(walkabout=npc_walkabout, say_text="Hello!")
tilemap.npcs = [npc]

viewport = render.Viewport((VIEWPORT_X, VIEWPORT_Y))
game_blueprint = game.Game(
                           tilemap=tilemap,
                           human_player=human,
                           viewport=viewport
                          )

# runtime
game_blueprint.start_loop()

