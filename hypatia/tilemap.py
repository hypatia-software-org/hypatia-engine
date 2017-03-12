import os
import json
import pygame

from enum import IntEnum
from hypatia.tilesheet import Tilesheet


class TilemapTileFlags(IntEnum):
    NONE = 0
    OBJECT = 1
    STATIC_NPC = 2
    TELEPORTER = 4

class Tilemap:
    def __init__(self, layers, player_data):
        self.layer_data = layers
        self.player_data = player_data

        self.height_in_tiles = len(self.layer_data[0])
        self.width_in_tiles = len(self.layer_data[0][0])

        # assume all tilesheets are the same tile_{width,height}
        tilesheet = self.layer_data[0][0][0]["tilesheet"]
        self.tile_width = tilesheet.tile_width
        self.tile_height = tilesheet.tile_height
        self.width = self.tile_width * self.width_in_tiles
        self.height = self.tile_height * self.height_in_tiles

        self.have_animated_tiles = False

        self.layer_tiles = []

    @classmethod
    def from_resource_pack(cls, resourcepack, mapname):
        raw_data = json.load(resourcepack.open(os.path.join("/maps", mapname + os.extsep + "json")))

        layers = []
        tilesheets = []

        for tilesheet_data in raw_data["tilesheets"]:
            tilesheet = Tilesheet.from_resource_pack(resourcepack, tilesheet_data["name"])
            tilesheets.append(tilesheet)

        for layer_raw_data in raw_data['layers']:
            layer_data = []

            for row_idx, row_raw_data in enumerate(layer_raw_data):
                row_data = []

                for column_idx, column_raw_data in enumerate(row_raw_data):
                    if column_raw_data.strip() == "-1":
                        tilesheet_idx = 0
                        tile_id = -1

                    else:
                        (tilesheet_idx, tile_id) = [int(a) for a in column_raw_data.strip().split(":")]

                    tilesheet = tilesheets[tilesheet_idx]

                    tilepos_str = f"{column_idx:d},{row_idx:d}"
                    tileflags = TilemapTileFlags.NONE
                    tile_metadata = {}
                    if "tile_metadata" in raw_data and tilepos_str in raw_data["tile_metadata"]:
                        tile_metadata = raw_data["tile_metadata"][tilepos_str]
                        flags = tile_metadata["flags"] if "flags" in tile_metadata else []
                        for flag in flags:
                            tileflags = tileflags | TilemapTileFlags[flag]

                    column_data = {
                        "tilesheet": tilesheet,
                        "tile_id": tile_id,
                        "tile_flags": tileflags,
                        "metadata": tile_metadata,
                    }

                    row_data.append(column_data)

                layer_data.append(row_data)

            layers.append(layer_data)

        if raw_data["player"]["layer"] >= len(layers):
            empty_tile = {
                "tilesheet": tilesheets[0],
                "tile_id": -1,
                "tile_flags": TilemapTileFlags.NONE,
                "metadata": {}
            }

            empty_layer = [[empty_tile for _ in range(0, a)] for a in range(0, len(layers[0]))]
            layers.append(empty_layer)

        return cls(layers, raw_data["player"])

    def _render_layer_tiles_to_surfaces(self, timedelta):
        """Renders self.layer_tiles to an array of surfaces and returns 
        that array.
        """

        layer_surfaces = []
        for layer_idx, layer_tiles in enumerate(self.layer_tiles):
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

    def get_solid_rects(self):
        rects = []

        for layer_idx, layer_data in enumerate(self.layer_tiles):
            for row_idx, row_data in enumerate(layer_data):
                for column_idx, tile_data in enumerate(row_data):
                    current_y = row_idx * self.tile_height
                    current_x = column_idx * self.tile_width

                    rect = pygame.Rect(current_x, current_y, self.tile_width, self.tile_height)
                    if tile_data["tile"].is_solid():
                        rects.append(rect)

        return rects

    def update(self, timedelta):
        if len(self.layer_tiles) is 0:
            self.layer_tiles = []

            for layer_idx, layer_data in enumerate(self.layer_data):
                layer_tiles = []

                for row_idx, row_data in enumerate(layer_data):
                    row_tiles = []

                    for column_idx, tile_data in enumerate(row_data):
                        tile = tile_data["tilesheet"].get_tile(tile_data["tile_id"])

                        our_tile_data = {
                            "tile": tile,
                            "flags": tile_data["tile_flags"] if "tile_flags" in tile_data else TilemapTileFlags.NONE,
                            "metadata": tile_data["metadata"] if "metadata" in tile_data else {},
                        }

                        if "tile_flags" in tile_data:
                            if (tile_data["tile_flags"] & TilemapTileFlags.OBJECT) == TilemapTileFlags.OBJECT:
                                our_tile_data["actual_tile"] = tile
                                from hypatia.character import TileNPCCharacter
                                character = TileNPCCharacter(our_tile_data)
                                our_tile_data["tile"] = character

                        row_tiles.append(our_tile_data)

                    layer_tiles.append(row_tiles)

                self.layer_tiles.append(layer_tiles)

        output_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        layer_surfaces = self._render_layer_tiles_to_surfaces(timedelta)

        return layer_surfaces