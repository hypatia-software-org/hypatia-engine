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

class MockGame:
    def __init__(self):
        self.display = MockDisplay()
        self.clock = MockClock()
        self.gameconfig = {
            "camera_resolution": (1, 1),
        }
