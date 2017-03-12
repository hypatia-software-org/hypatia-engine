import pygame

from hypatia.resources import ResourcePack


class MockPopulatedResourcePack(ResourcePack):
    def __init__(self):
        super().__init__()

        self.content = {
            "type": "dir",
            "content": {
                "testfile": {
                    "type": "file",
                    "content": b"Hello world!"
                },
                "testdir": {
                    "type": "dir",
                    "content": {
                        "subfile": {
                            "type": "file",
                            "content": b"Hello again!"
                        }
                    }
                }
            }
        }

class MockClock:
    def get_time(self):
        return 1

class MockDisplay:
    def get_size(self):
        return (800, 600)

    def get_width(self):
        return 800

    def get_height(self):
        return 600


class MockGame:
    def __init__(self):
        self.display = MockDisplay()
        self.clock = MockClock()

        pygame.font.init()
        self.font = pygame.font.Font(None, 24)

        self.gameconfig = {
            "camera_resolution": (2, 2),
        }
