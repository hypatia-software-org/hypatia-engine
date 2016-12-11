import pygame

class Camera(pygame.Surface):
    def __init__(self, source_res, camera_res, target_res):
        self.source_res = source_res
        self.source_surface = pygame.Surface(source_res)

        self.camera_res = camera_res

        self.target_res = target_res

        self._position = (0, 0)

        super().__init__(target_res)

    def update(self):
        rect = pygame.Rect(self._position, self.camera_res)
        source = self.source_surface.subsurface(rect)

        scaled = pygame.transform.scale(source, self.target_res)

        self.blit(source, (0, 0))

    def move(self, pos_tuple):
        assert len(pos_tuple) == 2

        self._position = pos_tuple
        self.update()


