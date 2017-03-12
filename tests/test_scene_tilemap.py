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

        game = MockGame()
        scene = TilemapScene(game, resourcepack, "testmap", "test")

        assert scene.camera.source_res == (scene.tilemap.width, scene.tilemap.height)
        assert scene.camera.camera_res == (2, 2)
        assert scene.camera.target_res == game.display.get_size()

    def test_update(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        game = MockGame()
        scene = TilemapScene(game, resourcepack, "testmap", "test")
        scene.camera.move((3, 3))
        scene.update()

        test_surface = pygame.Surface((800, 600))
        test_surface.fill((255, 0, 0), pygame.Rect(0, 0, 400, 300))

        assert compare_surfaces(scene.surface, test_surface)

    def test_moving_player(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        resourcepack = FilesystemResourcePack(dir_path)

        game = MockGame()
        scene = TilemapScene(game, resourcepack, "testmap", "test")

        scene.update()

        test_surface_one = pygame.Surface((800, 600))
        test_surface_one.fill((255, 0, 0), pygame.Rect(0, 0, 400, 300))
        assert compare_surfaces(scene.surface, test_surface_one)

        scene.player_movement_speed = [1, 1]
        scene.update()

        test_surface_two = pygame.Surface((800, 600))
        test_surface_two.fill((0, 127, 127), pygame.Rect(0, 0, 400, 300))
        test_surface_two.fill((255, 0, 0), pygame.Rect(400, 300, 400, 300))

        assert compare_surfaces(scene.surface, test_surface_two)
