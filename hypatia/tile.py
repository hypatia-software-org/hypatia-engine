import pygame

from enum import IntEnum


class TileFlags(IntEnum):
    NONE = 0
    SOLID = 1
    DESTRUCTIBLE = 2

class Tile(pygame.sprite.Sprite):
    def __init__(self, tilesheet, tile_id, flags):
        super().__init__()

        self.tilesheet = tilesheet
        self.tile_id = tile_id
        self.tile_flags = flags

        self.image = pygame.Surface((tilesheet.tile_width, tilesheet.tile_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self, timedelta):
        # allow blank tiles
        if self.tile_id != -1:
            self.image = self.tilesheet.get_tile_subsurface(self.tile_id)
            self.rect = self.image.get_rect()

    def is_solid(self):
        return self.tile_flags & TileFlags.SOLID == TileFlags.SOLID

    def is_destructible(self):
        return self.tile_flags & TileFlags.DESTRUCTIBLE == TileFlags.DESTRUCTIBLE

