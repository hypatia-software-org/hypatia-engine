import os
import pygame

from hypatia.utils import compare_surfaces
from hypatia.resources.filesystem import FilesystemResourcePack
from hypatia.tilesheet import Tilesheet
from hypatia.tilemap import Tilemap, TilemapTileFlags

class TestTilemap:
    def test_creation_from_passed_data(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilesheet = Tilesheet.from_resource_pack(resourcepack, "test")

        data = {
            "player": {
                "layer": 0,
                "start_pos": [0, 0],
            },
            "layers": [
                [
                    ["0:0", "0:1"],
                    ["0:2", "0:3"],
                ],
            ],
            "tilesheets": [
                {
                    "name": "test",
                },
            ],
        }

        tilemap = Tilemap(data, [tilesheet])

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


        data = {
            "player": {
                "layer": 0,
                "start_pos": [0, 0],
            },
            "layers": [
                [
                    ["0:0", "0:1"],
                    ["0:2", "0:3"],
                ],
            ],
            "tilesheets": [
                {
                    "name": "test",
                },
            ],
        }

        tilemap = Tilemap(data, [tilesheet])

        output_surface = pygame.Surface((2, 2))
        output_surfaces = tilemap.update(0)
        for i in output_surfaces:
            output_surface.blit(i, (0, 0))

        test_surface = pygame.Surface((2, 2))
        test_surface.fill((255, 0, 0), pygame.Rect(1, 0, 1, 1))
        test_surface.fill((0, 255, 0), pygame.Rect(0, 1, 1, 1))
        test_surface.fill((0, 0, 255), pygame.Rect(1, 1, 1, 1))

        assert compare_surfaces(output_surface, test_surface)

    def test_rendering_multiple_layers(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilemap = Tilemap.from_resource_pack(resourcepack, "testmap")
        output_surface = pygame.Surface((10, 10))
        output_surfaces = tilemap.update(0)
        for i in output_surfaces:
            output_surface.blit(i, (0, 0))

        test_surface = pygame.Surface((10, 10))
        test_surface.fill((0, 0, 0))
        test_surface.fill((255, 0, 0), pygame.Rect(3, 3, 4, 4))
        test_surface.fill((0, 255, 0), pygame.Rect(4, 4, 2, 2))
        test_surface.fill((0, 127, 127), pygame.Rect(0, 0, 1, 1))

        assert compare_surfaces(output_surface, test_surface)

    def test_tilemap_tile_flags(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilemap = Tilemap.from_resource_pack(resourcepack, "testmap")
        tilemap.update(0)

        assert tilemap.tile_data[0][1][1]["flags"] & TilemapTileFlags.STATIC_NPC == TilemapTileFlags.STATIC_NPC

    def test_tilemap_tile_metadata(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilemap = Tilemap.from_resource_pack(resourcepack, "testmap")
        tilemap.update(0)

        assert "lines_to_say" in tilemap.tile_data[0][1][1]["metadata"] 
