import pygame

from hypatia.utils import compare_surfaces, keyname_to_keysym, keysym_to_keyname

class TestCompareSurfaces:
    def test_compare_same_surface(self):
        s = pygame.Surface((1, 1))
        s.fill((0, 0, 0))

        assert compare_surfaces(s, s)

    def test_compare_identical_surfaces(self):
        surface_one = pygame.Surface((1, 1))
        surface_one.fill((0, 0, 0))

        surface_two = pygame.Surface((1, 1))
        surface_two.fill((0, 0, 0))

        assert compare_surfaces(surface_one, surface_two)

    def test_compare_different_size_surfaces(self):
        surface_one = pygame.Surface((1, 1))
        surface_one.fill((0, 0, 0))

        surface_two = pygame.Surface((2, 2))
        surface_two.fill((0, 0, 0))

        assert compare_surfaces(surface_one, surface_two) == False

    def test_compare_different_surfaces(self):
        surface_one = pygame.Surface((1, 1))
        surface_one.fill((0, 0, 0))

        surface_two = pygame.Surface((1, 1))
        surface_two.fill((255, 255, 255))

        assert compare_surfaces(surface_one, surface_two) == False

class TestKeysymToKeyname:
    def test_keysym_to_keyname(self):
        assert keysym_to_keyname(pygame.K_UP) == "K_UP"

class TestKeynameToKeysym:
    def test_keyname_to_keysym(self):
        assert keyname_to_keysym("K_UP") == pygame.K_UP
