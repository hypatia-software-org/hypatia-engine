import os
import pygame

from hypatia.utils import compare_surfaces
from hypatia.resources.filesystem import FilesystemResourcePack
from hypatia.tilesheet import Tilesheet
from hypatia.tilemap import Tilemap, TilemapTileFlags

class TestTileNPCCharacter:
    def test_interact_returns_lines(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilemap = Tilemap.from_resource_pack(resourcepack, "testmap")
        tilemap.update(0)

        data = tilemap.layer_tiles[0][1][1]["tile"].interact()

        assert "say" in data
        assert "test" in data["say"]

