"""Dialog, text tools.

All very experimental. Highly subject to change.

"""


import pygame


class DialogBox(object):

    def __init__(self, follows, message):
        """
        
        Args:
          message (str): --
        
        """
        
        self.follows = follows
        self.message = message.upper()
        self.viewport_lines = 4
 
    def blit(self, to_surface, font, max_width):
        text_surface = font.render(
                                   self.message,
                                   False,
                                   (255, 255, 255),
                                   (0, 0, 0)
                                  )
        to_surface.blit(text_surface, (0, 0))
