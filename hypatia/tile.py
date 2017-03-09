import pygame

from enum import IntEnum


class TileFlags(IntEnum):
    NONE = 0
    SOLID = 1
    DESTRUCTIBLE = 2

class Tile(pygame.Surface):
    def __init__(self, tilesheet, tile_id, flags):
        
        self.tilesheet = tilesheet
        self.tile_id = tile_id
        self.tile_flags = flags

        super().__init__((tilesheet.tile_width, tilesheet.tile_height), pygame.SRCALPHA)

    def update(self):
        # allow blank tiles
        if self.tile_id != -1:
            self.blit(self.tilesheet.get_tile_subsurface(self.tile_id), (0, 0))

    def is_solid(self):
        return self.tile_flags & TileFlags.SOLID == TileFlags.SOLID

    def is_destructible(self):
        return self.tile_flags & TileFlags.DESTRUCTIBLE == TileFlags.DESTRUCTIBLE

