import os
import pygame
import pytest

from hypatia.resources.filesystem import FilesystemResourcePack
from hypatia.scenes.tilemap import TilemapScene
from hypatia.tilemap import Tilemap 
from hypatia.test_mocks import MockGame
from hypatia.utils import compare_surfaces


class TestTilemapScene:
    def test_camera_creation(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilemap = Tilemap.from_resource_pack(resourcepack, "testmap")

        game = MockGame()
        scene = TilemapScene(game, tilemap)

        assert scene.camera.source_res == (tilemap.width, tilemap.height)
        assert scene.camera.camera_res == (1, 1)
        assert scene.camera.target_res == game.display.get_size()

    def test_update(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        tilemap = Tilemap.from_resource_pack(resourcepack, "testmap")

        game = MockGame()
        scene = TilemapScene(game, tilemap)
        scene.camera.move((3, 3))
        scene.update()

        test_surface = pygame.Surface((800, 600))
        test_surface.fill((255, 0, 0))

        assert compare_surfaces(scene.surface, test_surface)