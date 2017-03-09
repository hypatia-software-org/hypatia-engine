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
