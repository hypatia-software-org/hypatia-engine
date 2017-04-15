import pygame

from hypatia import class_get, class_default
from hypatia.utils import keyname_to_keysym, wrap_line, blur_surface

@class_default
class TextBoxScene(class_get("Scene")):
    def __init__(self, game, lines):
        super().__init__(game)

        self.lines = lines
        self.current_line = 0

    def update(self):
        self.create_surface()
        self.surface.fill((0, 0, 0))

        # get the previous scene as a background
        try:
            self.game.scene_stack[-2].update()
            bg = self.game.scene_stack[-2].surface
            self.surface.blit(bg, (0, 0))

        except KeyError:
            pass

        except AttributeError:
            pass

        width = self.game.display.get_width() - 20 - 20
        line = self.lines[self.current_line]
        lines = wrap_line(self.game.font, width, line)
        
        height = sum([self.game.font.size(line)[1] for line in lines]) + ((len(lines) - 1) * 10)

        ypos = self.game.display.get_height() - height - 20
        rect = pygame.Rect(10, ypos, width + 20, height)
        self.surface.fill((0, 0, 0), rect)

        for idx, line in enumerate(lines):
            surface = self.game.font.render(line, True, (255, 255, 255))
            self.surface.blit(surface, (20, ypos))
            ypos += surface.get_height() + 10

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == keyname_to_keysym(self.game.userconfig["keymaps"]["interact"]):
                if self.current_line + 1 == len(self.lines):
                    self.game.scene_pop()

                else:
                    self.current_line += 1

