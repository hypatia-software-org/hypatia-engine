import pygame

from hypatia import class_get, class_default
from hypatia.utils import wrap_line

@class_default
class BottomLevelScene(class_get("Scene")):
    def update(self):
        self.create_surface()
        self.surface.fill((0, 0, 0))

        lines = [
            "There are no scenes on the stack.",
            "",
            "Keys: ESC to die, F1 to push the starting tilemap scene."
        ]

        final_lines = []
        for idx, line in enumerate(lines):
            lines = wrap_line(self.game.font, self.game.display.get_width() - 20, line)
            for i in lines:
                final_lines.append(i)

        ypos = 10
        for idx, line in enumerate(final_lines):
            text = self.game.font.render(line, True, (255, 255, 255))
            self.surface.blit(text, (10, ypos))
            ypos += text.get_height() + 5


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.running = False

            elif event.key == pygame.K_F1:
                self.game.scene_pop()
                self.game.scene_push(class_get("TilemapScene"), self.game.resourcepack, self.game.gameconfig['starting_tilemap'], self.game.gameconfig["player_character"])
