import pygame

from hypatia import class_get, class_default

@class_default
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

        self.blit(scaled, (0, 0))

    def move(self, pos_tuple):
        assert len(pos_tuple) == 2

        self._position = pos_tuple
        self.update()

    def center_on(self, focal_rect):
        new_view_rect = pygame.Rect(self._position, self.camera_res)
        new_view_rect.center = focal_rect.center

        if new_view_rect.left < 0:
            new_view_rect.left = 0

        if new_view_rect.top < 0:
            new_view_rect.top = 0
        
        if new_view_rect.bottom > self.source_res[1]:
            new_view_rect.bottom = self.source_res[1]
        
        if new_view_rect.right > self.source_res[0]:
            new_view_rect.right = self.source_res[0]

        self._position = new_view_rect.topleft
        self.update()


