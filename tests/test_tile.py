import os
import pytest
import pygame

from hypatia.utils import compare_surfaces
from hypatia.tile import Tile, TileFlags
from hypatia.tilesheet import Tilesheet


class TestTile:
    def test_single_flag(self):
        tilesheet = Tilesheet(pygame.Surface((2, 2)), 1, 1)
        tile = Tile(tilesheet, 0, TileFlags.SOLID)

        assert tile.is_solid() is True

    def test_multiple_flags(self):
        tilesheet = Tilesheet(pygame.Surface((2, 2)), 1, 1)
        tile = Tile(tilesheet, 0, TileFlags.SOLID | TileFlags.DESTRUCTIBLE)

        assert tile.is_solid() is True
        assert tile.is_destructible() is True

    def test_blank_tile_is_transparent(self):
        tilesheet = Tilesheet(pygame.Surface((2, 2)), 1, 1)
        tile = Tile(tilesheet, -1, TileFlags.NONE)
        tile.update(0)

        test_surface = pygame.Surface((1, 1), pygame.SRCALPHA)

        assert compare_surfaces(tile.image, test_surface)

    def test_tile_blit(self):
        tilesheet_surface = pygame.Surface((2, 2))

        # fill the tilesheet surface with colors 
        tilesheet_surface.fill((255, 0, 0), pygame.Rect(0, 0, 1, 1))
        tilesheet_surface.fill((0, 255, 0), pygame.Rect(1, 0, 1, 1))
        tilesheet_surface.fill((0, 0, 255), pygame.Rect(0, 1, 1, 1))
        tilesheet_surface.fill((255, 255, 255), pygame.Rect(1, 1, 1, 1))

        tilesheet = Tilesheet(tilesheet_surface, 1, 1)
        tile = Tile(tilesheet, 1, TileFlags.NONE)
        tile.update(0)

        test_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        test_surface.fill((0, 255, 0))

        assert compare_surfaces(tile.image, test_surface)