import pygame
from engine import tiles
from engine import entities
from engine import render


# ENGINE: tiles
tiles.new_tilemap('debug')
tilemap = tiles.load_tilemap('debug')

for i, layer in enumerate(tilemap.layers):
    pygame.image.save(layer, 'layer-%d.png' % i)

assert tilemap[(0, 0)] == ['requires_boat', 'impass_all']

print(tilemap.name)
print(tilemap.properties[0])
print(tilemap.get_properties)

# ENGINE: entities

# walkabout; test saving paricular anims or wahtevs
walkabout = entities.Walkabout('guy')

# ENGINE: render

render.render('debug')

