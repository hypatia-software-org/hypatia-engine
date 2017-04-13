import pygame

from enum import IntFlag
from hypatia.animatedsprite import Frame, AnimatedSprite


class TileFlags(IntFlag):
    NONE = 0
    SOLID = 1
    DESTRUCTIBLE = 2
    ANIMATED = 4

class Tile(pygame.sprite.Sprite):
    def __init__(self, tilesheet, tile_id, flags, metadata={}):
        super().__init__()

        self.tilesheet = tilesheet
        self.tile_id = tile_id
        self.tile_flags = flags
        self.tile_metadata = metadata

        self.image = pygame.Surface((tilesheet.tile_width, tilesheet.tile_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        if self.is_animated():
            frames = []
            duration = 0
            for idx, (tileid, tileduration) in enumerate(metadata["animation"]):
                surface = self.tilesheet.get_tile_subsurface(tileid)
                frames.append(Frame(surface, duration, tileduration))
                duration += tileduration

            self.animatedsprite = AnimatedSprite(frames)

    def update(self, timedelta):
        # allow blank tiles
        if self.tile_id != -1:
            if self.is_animated():
                self.animatedsprite.update(timedelta)
                self.image = self.animatedsprite.image

            else:
                self.image = self.tilesheet.get_tile_subsurface(self.tile_id)

            self.rect = self.image.get_rect()

    def is_solid(self):
        return TileFlags.SOLID in self.tile_flags

    def is_destructible(self):
        return TileFlags.DESTRUCTIBLE in self.tile_flags

    def is_animated(self):
        return TileFlags.ANIMATED in self.tile_flags

