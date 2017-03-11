import os
import json
import pygame

from hypatia.tilesheet import Tilesheet


class Tilemap:
    def __init__(self, layers):
        self.layer_data = layers

        self.height_in_tiles = len(self.layer_data[0])
        self.width_in_tiles = len(self.layer_data[0][0])

        # assume all tilesheets are the same tile_{width,height}
        tilesheet = self.layer_data[0][0][0]["tilesheet"]
        self.width = tilesheet.tile_width * self.width_in_tiles
        self.height = tilesheet.tile_height * self.height_in_tiles

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

                    column_data = {
                        "tilesheet": tilesheet,
                        "tile_id": tile_id,
                    }
                    
                    row_data.append(column_data)
                
                layer_data.append(row_data)

            layers.append(layer_data)

        return cls(layers)

    def _render_layer_tiles_to_surfaces(self, timedelta):
        """Renders self.layer_tiles to an array of surfaces and returns 
        that array.
        """

        layer_surfaces = []
        for layer_idx, layer_tiles in enumerate(self.layer_tiles):
            layer_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            for row_idx, row_data in enumerate(layer_tiles):
                for column_idx, tile in enumerate(row_data):
                    pos = (
                        column_idx * tile.tilesheet.tile_width,
                        row_idx * tile.tilesheet.tile_height
                    )

                    tile.update(timedelta)

                    layer_surface.blit(tile.image, pos)

            layer_surfaces.append(layer_surface)

        return layer_surfaces

    def update(self, timedelta):
        if len(self.layer_tiles) is 0:
            self.layer_tiles = []

            for layer_idx, layer_data in enumerate(self.layer_data):
                layer_tiles = []

                for row_idx, row_data in enumerate(layer_data):
                    row_tiles = []

                    for column_idx, tile_data in enumerate(row_data):
                        tile = tile_data["tilesheet"].get_tile(tile_data["tile_id"])
                        row_tiles.append(tile)

                    layer_tiles.append(row_tiles)

                self.layer_tiles.append(layer_tiles)

        output_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        layer_surfaces = self._render_layer_tiles_to_surfaces(timedelta)

        for layer_idx, layer_surface in enumerate(layer_surfaces):
            output_surface.blit(layer_surface, (0, 0))

        return output_surface
