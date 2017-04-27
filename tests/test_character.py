import os
import pygame

from hypatia.utils import compare_surfaces
from hypatia.test_mocks import MockGame
from hypatia.resources.filesystem import FilesystemResourcePack
from hypatia.tilesheet import Tilesheet
from hypatia.tilemap import Tilemap, TilemapTileFlags

class TestTileNPCCharacter:
    def test_interact_returns_lines(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        game = MockGame()

        tilemap = Tilemap.from_resource_pack(resourcepack, "testmap")
        tilemap.update(0)

        data = tilemap.tile_data[0][1][1]["tile"].interact(game)

        assert "say" in data
        assert "test" in data["say"]

