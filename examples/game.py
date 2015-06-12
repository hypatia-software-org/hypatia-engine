# examples/game.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""This is a game demo which showcases Hypatia's features.

"""

import os
import sys
import collections

import pygame
from pygame.locals import *

from hypatia import tiles
from hypatia import sprites
from hypatia import render
from hypatia import player
from hypatia import game

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
game = game.Game(viewport=viewport)

# set human player
hat = sprites.Walkabout('hat')
human_walkabout = sprites.Walkabout('debug', children=[hat])
game.human_player = player.Player(walkabout=human_walkabout)

# set game tilemap
with open('map-string.txt') as f:
    blueprint_string = f.read()

tilemap = tiles.TileMap.from_string(blueprint_string)
#new_tilemap_string = tilemap.to_string()
#game.tilemap = tiles.TileMap.from_string(new_tilemap_string)
#print(game.tilemap.to_string())
game.tilemap = tilemap

# ... and set tilemap npcs
npc_walkabout = sprites.Walkabout('debug', position=(140, 140))

with open('npc-say.txt') as f:
    npc_say = f.read()

npc = player.Npc(walkabout=npc_walkabout, say_text=npc_say)
game.tilemap.npcs = [npc]

# finished!
game.start_loop()

