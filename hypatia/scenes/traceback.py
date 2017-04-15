import pygame

from hypatia import class_get, class_default
from hypatia.utils import wrap_line

@class_default
class TracebackScene(class_get("Scene")):
    def __init__(self, game, exception, traceback):
        super().__init__(game)

        self.exception = exception
        self.traceback = traceback

        msg = "Keys: ESC to die, F5 to resume last scene"
        self.msg_text = self.game.font.render(msg, True, (255, 255, 255))
        self.msg_height = self.msg_text.get_height() + 20

        tb_lines = []
        for idx, line in enumerate(self.traceback.split("\n")):
            lines = wrap_line(self.game.font, self.game.display.get_width() - 20, line)
            for i in lines:
                tb_lines.append(i)

        tb_height = sum([self.game.font.size(line)[1] for line in tb_lines]) + (len(tb_lines) * 5) 

        camera_size = (
            self.game.display.get_width(),
            max(self.game.display.get_height() - self.msg_height, tb_height)
        )

        target_size = (
            self.game.display.get_width(),
            self.game.display.get_height() - self.msg_height
        )

        self.camera = class_get("Camera")(camera_size, target_size, target_size)
        self.camera.source_surface.fill((127, 26, 26))

        ypos = 10
        for idx, line in enumerate(tb_lines):
            text = self.game.font.render(line, True, (255, 255, 255))
            self.camera.source_surface.blit(text, (10, ypos))
            ypos += text.get_height() + 5

        self.movement = 0

    def update(self):
        self.create_surface()
        self.surface.fill((127, 26, 26))

        if self.movement > 0:
            if self.camera._position[1] - self.camera.source_surface.get_height() > 0:
                self.camera.move((0, self.camera._position[1] + 1))

        elif self.movement < 0:
            if self.camera._position[1] > 0:
                self.camera.move((0, self.camera._position[1] - 1))

        self.camera.update()
        self.surface.blit(self.msg_text, (0, 10))
        self.surface.blit(self.camera, (0, self.msg_height))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.movement = 1

            elif event.key == pygame.K_UP:
                self.movement = -1

            elif event.key == pygame.K_ESCAPE:
                self.game.running = False
            
            elif event.key == pygame.K_F5:
                self.game.scene_pop()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                self.movement = 0

