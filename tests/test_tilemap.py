import os
import pygame

from hypatia.utils import compare_surfaces
from hypatia.resources.filesystem import FilesystemResourcePack
from hypatia.tilesheet import Tilesheet
from hypatia.tilemap import Tilemap

class TestTilemap:
    def test_creation_from_passed_data(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilesheet = Tilesheet.from_resource_pack(resourcepack, "test")

        layer_data = [
            [
                [{"tilesheet": tilesheet, "tile_id": 0}, {"tilesheet": tilesheet, "tile_id": 1}],
                [{"tilesheet": tilesheet, "tile_id": 2}, {"tilesheet": tilesheet, "tile_id": 3}],
            ]
        ]

        tilemap = Tilemap(layer_data)

        assert tilemap.width == 2
        assert tilemap.height == 2

    def test_creation_from_resource_pack(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilemap = Tilemap.from_resource_pack(resourcepack, "testmap")

        assert tilemap.width == 10
        assert tilemap.height == 10

    def test_rendering_one_layer(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilesheet = Tilesheet.from_resource_pack(resourcepack, "test")

        layer_data = [
            [
                [{"tilesheet": tilesheet, "tile_id": 0}, {"tilesheet": tilesheet, "tile_id": 1}],
                [{"tilesheet": tilesheet, "tile_id": 2}, {"tilesheet": tilesheet, "tile_id": 3}],
            ]
        ]

        tilemap = Tilemap(layer_data)
        output_surface = tilemap.update(0)

        # the outputted tilemap should be identical to the tilesheet image itself
        assert compare_surfaces(output_surface, tilesheet.surface)

    def test_rendering_multiple_layers(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilemap = Tilemap.from_resource_pack(resourcepack, "testmap")
        output_surface = tilemap.update(0)

        test_surface = pygame.Surface((10, 10))
        test_surface.fill((0, 0, 0))
        test_surface.fill((255, 0, 0), pygame.Rect(3, 3, 4, 4))
        test_surface.fill((0, 255, 0), pygame.Rect(4, 4, 2, 2))

        assert compare_surfaces(output_surface, test_surface)
