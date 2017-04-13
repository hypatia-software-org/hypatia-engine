import os
import json
import pygame

from enum import IntFlag
from hypatia.tilesheet import Tilesheet


class TilemapTileFlags(IntFlag):
    NONE = 0
    OBJECT = 1
    STATIC_NPC = 2
    TELEPORTER = 4
    CUSTOM_CODE = 8

    @classmethod
    def flags_to_str_array(cls, flags):
        out = []

        for flag in cls:
            if flag is cls.NONE:
                continue

            if flag in flags:
                out.append(flag.name)

        return out

class Tilemap:
    def __init__(self, tilemap_obj, tilesheets):
        self.raw_tile_data = tilemap_obj
        self.player_data = self.raw_tile_data["player"] if "player" in self.raw_tile_data else {}
        self.tilesheets = tilesheets

        self.height_in_tiles = len(self.raw_tile_data["layers"][0])
        self.width_in_tiles = len(self.raw_tile_data["layers"][0][0])

        # assume all tilesheets are the same tile_{width,height}
        self.tile_width = self.tilesheets[0].tile_width
        self.tile_height = self.tilesheets[0].tile_height
        self.width = self.tile_width * self.width_in_tiles
        self.height = self.tile_height * self.height_in_tiles

        self.have_animated_tiles = False

        self.empty_tile = {
            "tilesheet": self.tilesheets[0],
            "tile_id": -1,
            "flags": TilemapTileFlags.NONE,
            "metadata": {},
            "tile": self.tilesheets[0].get_tile(-1),
            "actual_tile": self.tilesheets[0].get_tile(-1),
        }

        self.tile_data = self.generate_tile_data()

    @classmethod
    def from_resource_pack(cls, resourcepack, mapname):
        raw_data = json.load(resourcepack.open(resourcepack.join("/maps", mapname + os.extsep + "json")))

        tilesheets = []
        for tilesheet_data in raw_data["tilesheets"]:
            tilesheet = Tilesheet.from_resource_pack(resourcepack, tilesheet_data["name"])
            tilesheets.append(tilesheet)

        return cls(raw_data, tilesheets)

    def generate_tile_data(self):
        layers = []

        for layer_idx, layer_data in enumerate(self.raw_tile_data["layers"]):
            layer_tiles = []

            for row_idx, row_data in enumerate(layer_data):
                row_tiles = []

                for column_idx, raw_tile in enumerate(row_data):
                    tile_data = {}

                    if raw_tile.strip() == "-1":
                        tile_data = self.empty_tile

                    else:
                        (tilesheet_id, tile_id) = [int(a) for a in raw_tile.strip().split(":")]

                        tile_pos_str = f"{column_idx:d},{row_idx:d}"
                        tile_mapflags = TilemapTileFlags.NONE
                        tile_metadata = {}
                        if "tile_metadata" in self.raw_tile_data and tile_pos_str in self.raw_tile_data["tile_metadata"]:
                            tile_metadata = self.raw_tile_data["tile_metadata"][tile_pos_str]

                            flags = tile_metadata["flags"] if "flags" in tile_metadata else []
                            for flag in flags:
                                tile_mapflags = tile_mapflags | TilemapTileFlags[flag]

                        tile_data["flags"] = tile_mapflags
                        tile_data["metadata"] = tile_metadata

                        tilesheet = self.tilesheets[tilesheet_id]
                        tile_data["tilesheet"] = tilesheet

                        tile = tilesheet.get_tile(tile_id)
                        tile_data["actual_tile"] = tile

                        if TilemapTileFlags.OBJECT in tile_mapflags:
                            from hypatia.character import TileNPCCharacter
                            character = TileNPCCharacter(tile_data)
                            tile_data["tile"] = character
                        else:
                            tile_data["tile"] = tile

                    row_tiles.append(tile_data)

                layer_tiles.append(row_tiles)

            layers.append(layer_tiles)

        if self.raw_tile_data["player"]["layer"] >= len(layers):
            empty_layer = [[self.empty_tile for _ in range(0, self.width_in_tiles)] for _ in range(0, self.height_in_tiles)]
            layers.append(empty_layer)

        return layers

    def dump_to_obj(self):
        output = {
            "player": self.player_data,
            "layers": [],
            "tile_metadata": {},
            "tilesheets": self.raw_tile_data["tilesheets"],
        }

        for layer_idx, layer_data in enumerate(self.tile_data):
            layer_tiles = []

            for row_idx, row_data in enumerate(layer_data):
                row_tiles = []

                for column_idx, tile_data in enumerate(row_data):
                    tilesheet_id = self.tilesheets.index(tile_data["tilesheet"])
                    tile_id = tile_data["actual_tile"].tile_id

                    tile_str = f"{tilesheet_id:d}:{tile_id:d}"
                    tile_pos_str = f"{column_idx:d},{row_idx:d}"

                    if len(tile_data["metadata"].keys()) > 0 and tile_pos_str not in output["tile_metadata"]:
                        metadata = tile_data["metadata"]
                        flags = TilemapTileFlags.flags_to_str_array(tile_data["flags"])

                        if len(flags) > 0:
                            metadata["flags"] = flags

                        output["tile_metadata"][tile_pos_str] = metadata

                    row_tiles.append(tile_str)

                layer_tiles.append(row_tiles)

            output["layers"].append(layer_tiles)

        return output

    def get_solid_rects(self):
        rects = []

        for layer_idx, layer_data in enumerate(self.tile_data):
            for row_idx, row_data in enumerate(layer_data):
                for column_idx, tile_data in enumerate(row_data):
                    current_y = row_idx * self.tile_height
                    current_x = column_idx * self.tile_width

                    rect = pygame.Rect(current_x, current_y, self.tile_width, self.tile_height)
                    if tile_data["tile"].is_solid():
                        rects.append(rect)

        return rects

    def _render_layer_tiles_to_surfaces(self, timedelta):
        """Renders self.layer_tiles to an array of surfaces and returns 
        that array.
        """

        layer_surfaces = []

        for layer_idx, layer_tiles in enumerate(self.tile_data):
            layer_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            for row_idx, row_data in enumerate(layer_tiles):
                for column_idx, tile_data in enumerate(row_data):
                    pos = (
                        column_idx * tile_data["tile"].tilesheet.tile_width,
                        row_idx * tile_data["tile"].tilesheet.tile_height
                    )

                    tile_data["tile"].update(timedelta)

                    layer_surface.blit(tile_data["tile"].image, pos)

            layer_surfaces.append(layer_surface)

        return layer_surfaces

    def update(self, timedelta):
        layer_surfaces = self._render_layer_tiles_to_surfaces(timedelta)
        return layer_surfaces