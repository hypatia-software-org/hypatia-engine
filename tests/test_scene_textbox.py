import os
import pygame
import pytest

from hypatia.scenes.textbox import TextBoxScene
from hypatia.test_mocks import MockGame
from hypatia.utils import compare_surfaces


class TestTilemapScene:
    def test_textbox_one_line(self):
        game = MockGame()
        scene = TextBoxScene(game, ["test"])
        scene.update()

        test_surface = pygame.Surface((800, 600))
        text = game.font.render("test", True, (255, 255, 255))
        box_rect = pygame.Rect(10, 600 - 20 - text.get_height() - 10, 800 - 40, 10 + text.get_height() + 10)
        test_surface.fill((0, 0, 0), box_rect)
        test_surface.blit(text, (20, 600 - 20 - text.get_height()))

        assert compare_surfaces(scene.surface, test_surface)

    def test_text_two_lines(self):
        game = MockGame()
        scene = TextBoxScene(game, ["test", "test two"])
        scene.update()

        test_surface = pygame.Surface((800, 600))
        text = game.font.render("test", True, (255, 255, 255))
        box_rect = pygame.Rect(10, 600 - 20 - text.get_height() - 10, 800 - 40, 10 + text.get_height() + 10)
        test_surface.fill((0, 0, 0), box_rect)
        test_surface.blit(text, (20, 600 - 20 - text.get_height()))

        assert compare_surfaces(scene.surface, test_surface)

        # switch textbox to next line
        scene.current_line = 1
        scene.update()

        test_surface = pygame.Surface((800, 600))
        text = game.font.render("test two", True, (255, 255, 255))
        box_rect = pygame.Rect(10, 600 - 20 - text.get_height() - 10, 800 - 40, 10 + text.get_height() + 10)
        test_surface.fill((0, 0, 0), box_rect)
        test_surface.blit(text, (20, 600 - 20 - text.get_height()))

        assert compare_surfaces(scene.surface, test_surface)

        