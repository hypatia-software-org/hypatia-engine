import pygame

class Scene:
    def __init__(self, game):
        self.game = game
        self.create_surface()

    def create_surface(self):
        self.surface = pygame.Surface(self.game.display.get_size())

    def update(self):
        pass

    def handle_event(self, event):
        pass
