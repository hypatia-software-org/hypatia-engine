import pygame
from engine import tiles
from engine import entities
from engine import render


# ENGINE: tiles
tiles.new_tilemap('debug')
tilemap = tiles.load_tilemap('debug')
assert tilemap[(0, 0)] == ['requires_boat', 'impass_all']

print(tilemap.name)
print(tilemap.properties[0])
print(tilemap.get_properties)

# ENGINE: render

render.render('debug')

