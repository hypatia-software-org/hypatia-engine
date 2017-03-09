import os
import pytest

from hypatia.scenes import Scene
from hypatia.test_mocks import MockGame

class TestScene:
    def test_surface_creation(self):
        game = MockGame()
        scene = Scene(game)

        assert scene.surface.get_size() == game.display.get_size()