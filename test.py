import pygame
from engine import tiles
from engine import entities
from engine import render


# ENGINE: tiles
tiles.new_tilemap('debug')
tilemap = tiles.load_tilemap('debug')

print(tilemap.name)
render.render('debug')

