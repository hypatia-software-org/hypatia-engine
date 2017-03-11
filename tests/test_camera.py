import pygame

from hypatia.utils import compare_surfaces
from hypatia.camera import Camera

class TestCamera:
    def test_camera_surface_creation(self):
        c = Camera((1, 1), (1, 1), (2, 2))

        assert c.source_surface.get_size() == (1, 1)
        assert c.get_size() == (2, 2)

    def test_camera_subsurface(self):
        test_surface = pygame.Surface((1, 1))
        test_surface.fill((127, 127, 127))

        c = Camera((2, 1), (1, 1), (1, 1))
        c.fill((0, 0, 0))

        c.source_surface.blit(test_surface, (0, 0))
        c.update()

        assert compare_surfaces(test_surface, c)

    def test_camera_movement(self):
        test_surface = pygame.Surface((2, 1))
        test_surface.fill((255, 0, 0), pygame.Rect(0, 0, 1, 1))
        test_surface.fill((0, 255, 0), pygame.Rect(1, 0, 1, 1))

        c = Camera((2, 1), (1, 1), (1, 1))
        c.fill((0, 0, 0))

        c.source_surface.blit(test_surface, (0, 0))
        c.update()

        rect_one = pygame.Rect(0, 0, 1, 1)
        assert compare_surfaces(test_surface.subsurface(rect_one), c)

        # move the camera
        c.move((1, 0))

        rect_two = pygame.Rect(1, 0, 1, 1)
        assert compare_surfaces(test_surface.subsurface(rect_two), c)

    def test_camera_center_on(self):
        test_surface = pygame.Surface((3, 3))
        test_surface.fill((0, 0, 0))
        test_surface.fill((255, 0, 0), pygame.Rect(1, 1, 1, 1))

        c = Camera((3, 3), (1, 1), (1, 1))
        c.fill((0, 0, 0))

        c.source_surface.blit(test_surface, (0, 0))

        # test that the camera is on the black portion of the surface
        assert compare_surfaces(test_surface.subsurface(pygame.Rect(0, 0, 1, 1)), c)

        # move the camera to center on the surface
        focal_rect = test_surface.get_rect()
        c.center_on(focal_rect)

        # test that the camera now sees red
        assert compare_surfaces(test_surface.subsurface(pygame.Rect(1, 1, 1, 1)), c)
        