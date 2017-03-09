import os
import json
import pygame

from hypatia.tile import Tile, TileFlags

class Tilesheet:
    def __init__(self, surface, tile_width, tile_height, tile_flags):
        self.surface = surface
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_flags = tile_flags

        surfacewidth = self.surface.get_width()
        if surfacewidth % self.tile_width != 0:
            msg = f"Tilesheet surface width not a multiple of tile width (surface width: {surfacewidth}, tile width: {self.tile_width})"
            raise ValueError(msg)

        self.tile_count_x = surfacewidth / self.tile_width

        surfaceheight = self.surface.get_height()
        if surfaceheight % self.tile_width != 0:
            msg = f"Tilesheet surface height not a multiple of tile height (surface height: {surfaceheight}, tile height: {self.tile_height})"
            raise ValueError(msg)

        self.tile_count_y = surfaceheight / self.tile_height

    @classmethod
    def from_resource_pack(cls, resourcepack, tilesheet_name):
        imagefile = resourcepack.open(os.path.join("/tilesheets", tilesheet_name, "tilesheet.png"))
        surface = pygame.image.load(imagefile)

        metadata = json.load(resourcepack.open(os.path.join("/tilesheets", tilesheet_name, "tilesheet.json")))

        (tile_width, tile_height) = [int(a) for a in metadata['tile_size'].split("x")]
        tile_flags = metadata["flags"] if "flags" in metadata else {}

        return cls(surface, tile_width, tile_height, tile_flags)

    def get_tile(self, tile_id):
        flags = TileFlags.NONE
        if tile_id in self.tile_flags:
            for flag in self.tile_flags[tile_id]:
                flags = flags | TileFlags[flag]

        tile = Tile(self, tile_id, flags)
        return tile

    def get_tile_subsurface(self, tile_id):
        rect = pygame.Rect(self.get_tile_position(tile_id), (self.tile_width, self.tile_height))
        return self.surface.subsurface(rect)

    def get_tile_position(self, tile_id):
        tile_y = tile_id // self.tile_count_x
        tile_x = tile_id % self.tile_count_x 
        return ((tile_x * self.tile_width), tile_y * self.tile_height)
