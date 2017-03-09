import os
import pytest
import pygame

from hypatia.utils import compare_surfaces
from hypatia.resources.filesystem import FilesystemResourcePack
from hypatia.tilesheet import Tilesheet


class TestTilesheet:
    def test_from_passed_surface(self):
        tilesheet = Tilesheet(pygame.Surface((2, 2)), 1, 1)

        assert tilesheet.tile_width == 1
        assert tilesheet.tile_height == 1
        assert tilesheet.tile_count_x == 2
        assert tilesheet.tile_count_y == 2

    def test_failing_on_mismatched_size(self):
        with pytest.raises(ValueError):
            tilesheet = Tilesheet(pygame.Surface((3, 3)), 2, 2)

    def test_from_resource_pack(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'artifacts')
        resourcepack = FilesystemResourcePack(dir_path)

        tilesheet = Tilesheet.from_resource_pack(resourcepack, "/tilesheets/test")

        assert tilesheet.tile_width == 1
        assert tilesheet.tile_height == 1
        assert tilesheet.tile_count_x == 2
        assert tilesheet.tile_count_y == 2

    def test_get_tile_position(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'artifacts')
        resourcepack = FilesystemResourcePack(dir_path)

        tilesheet = Tilesheet.from_resource_pack(resourcepack, "/tilesheets/test")

        assert tilesheet.get_tile_position(1) == (1, 0)
        assert tilesheet.get_tile_position(3) == (1, 1)

    def test_get_tile_subsurface(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'artifacts')
        resourcepack = FilesystemResourcePack(dir_path)

        tilesheet = Tilesheet.from_resource_pack(resourcepack, "/tilesheets/test")

        test_surface = pygame.Surface((1, 1))
        test_surface.fill((0, 0, 0))

        assert compare_surfaces(tilesheet.get_tile_subsurface(0), test_surface)
