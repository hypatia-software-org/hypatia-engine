import pygame

from hypatia.scenes import Scene
from hypatia.camera import Camera


class TilemapScene(Scene):
    def __init__(self, game, tilemap):
        super().__init__(game)

        self.tilemap = tilemap
        self.camera = Camera(
            (self.tilemap.width, self.tilemap.height),
            self.game.gameconfig["camera_resolution"],
            self.game.display.get_size()
        )

    def update(self):
        self.create_surface()

        td = self.game.clock.get_time()

        self.camera.source_surface.fill((0, 0, 0))
        self.camera.source_surface.blit(self.tilemap.update(td), (0, 0))
        self.camera.update()

        self.surface.blit(self.camera, (0, 0))

    def handle_event(self, event):
        # TODO: write event handling code
        pass
