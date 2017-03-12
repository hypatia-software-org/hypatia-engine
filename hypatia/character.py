import os
import json
import pygame

from hypatia.animatedsprite import AnimatedSprite
from hypatia.tilemap import TilemapTileFlags

class Character(pygame.sprite.Sprite):
    SPRITE_TYPES = [
        "normal",
        "walk_north",
        "walk_south",
        "walk_east",
        "walk_west",
    ]

    def __init__(self, sprites):
        self.sprites = sprites
        self.active_sprite = "normal"

    @classmethod
    def from_resource_pack(cls, resourcepack, name):
        basepath = os.path.join("/sprites", name)
        sprites = {}

        for type in cls.SPRITE_TYPES:
            try:
                if resourcepack.exists(os.path.join(basepath, type + os.extsep + "gif")):
                    sprite = AnimatedSprite.from_resource_pack_gif(resourcepack, name, type)
                else:
                    sprite = AnimatedSprite.from_resource_pack_png(resourcepack, name, type)

                sprites[type] = sprite
            except:
                continue

        return cls(sprites)

    def update(self, timedelta):
        self.sprites[self.active_sprite].update(timedelta)
        self.image = self.sprites[self.active_sprite].image
        self.rect = self.sprites[self.active_sprite].rect

    def interact(self):
        return {}

class TileNPCCharacter(Character):
    def __init__(self, tile_data):
        self.tile_data = tile_data
        self.tilesheet = self.tile_data["actual_tile"].tilesheet

        sprites = {"normal": self.tile_data["actual_tile"]}
        super().__init__(sprites)

    def is_solid(self):
        return self.tile_data["actual_tile"].is_solid()

    def is_destructible(self):
        return self.tile_data["actual_tile"].is_destructible()

    def is_animated(self):
        return self.tile_data["actual_tile"].is_animated()

    def interact(self):
        if (self.tile_data["flags"] & TilemapTileFlags.STATIC_NPC) == TilemapTileFlags.STATIC_NPC: 
            return {
                "say": self.tile_data["metadata"]["lines_to_say"],
            }

        elif (self.tile_data["flags"] & TilemapTileFlags.TELEPORTER) == TilemapTileFlags.TELEPORTER:
            return {
                "teleport": {
                    "map": self.tile_data["metadata"]["teleport_map"],
                    "start_pos": self.tile_data["metadata"]["teleport_pos"] if "teleport_pos" in self.tile_data["metadata"] else None,
                }
            }

        return {}
