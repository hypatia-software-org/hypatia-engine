import os
import pygame
import pytest

from hypatia.utils import compare_surfaces
from hypatia.resources.filesystem import FilesystemResourcePack
from hypatia.animatedsprite import Frame, AnimatedSprite


class TestFrame:
    def test_frame(self):
        test_surface = pygame.Surface((1, 1))
        f = Frame(test_surface, 10, 10)

        assert f.start_time == 10
        assert f.duration == 10
        assert f.end_time == 20

class TestAnimatedSprite:
    def test_update_one_frame(self):
        test_surface = pygame.Surface((1, 1))
        test_surface.fill((255, 0, 0))

        frames = [
            Frame(test_surface, 0, 10)
        ]

        animsprite = AnimatedSprite(frames)

        # check that the first frame is there before an update
        assert compare_surfaces(animsprite.image, test_surface)

        # check that the sprite is still there after an update
        animsprite.update(1)
        assert compare_surfaces(animsprite.image, test_surface)

    def test_update_multiple_frames(self):
        test_surface_one = pygame.Surface((1, 1))
        test_surface_one.fill((255, 0, 0))
        test_surface_two = pygame.Surface((1, 1))
        test_surface_two.fill((0, 255, 0))

        frames = [
            Frame(test_surface_one, 0, 1),
            Frame(test_surface_two, 1, 1)
        ]

        animsprite = AnimatedSprite(frames)

        # check that the first frame is there before an update
        assert compare_surfaces(animsprite.image, test_surface_one)

        # check the second frame is there after an update
        animsprite.update(1)
        assert compare_surfaces(animsprite.image, test_surface_two)

    def test_loading_from_gif(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        fs = FilesystemResourcePack(dir_path)

        animsprite = AnimatedSprite.from_gif(fs.open("/sprites/test/normal.gif"))

        test_surface_one = pygame.Surface((1, 1))
        test_surface_one.fill((255, 0, 0))

        assert compare_surfaces(animsprite.image, test_surface_one)

        animsprite.update(100)

        test_surface_two = pygame.Surface((1, 1))
        test_surface_two.fill((0, 255, 0))

        assert compare_surfaces(animsprite.image, test_surface_two)
    
    def test_loading_from_resource_pack_gif(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        fs = FilesystemResourcePack(dir_path)

        animsprite = AnimatedSprite.from_resource_pack_gif(fs, "test", "normal")

        test_surface_one = pygame.Surface((1, 1))
        test_surface_one.fill((255, 0, 0))

        assert compare_surfaces(animsprite.image, test_surface_one)

        animsprite.update(100)

        test_surface_two = pygame.Surface((1, 1))
        test_surface_two.fill((0, 255, 0))

        assert compare_surfaces(animsprite.image, test_surface_two)

    def test_loading_from_resource_pack_png(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testgame', 'resources')
        fs = FilesystemResourcePack(dir_path)

        animsprite = AnimatedSprite.from_resource_pack_png(fs, "test_png", "normal")

        test_surface_one = pygame.Surface((1, 1))
        test_surface_one.fill((255, 0, 0))

        assert compare_surfaces(animsprite.image, test_surface_one)

        animsprite.update(100)

        test_surface_two = pygame.Surface((1, 1))
        test_surface_two.fill((0, 255, 0))

        assert compare_surfaces(animsprite.image, test_surface_two)
