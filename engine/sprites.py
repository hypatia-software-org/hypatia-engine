# engine/sprites.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia Engine and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""Sprites: sprite manipulation and presentation.

Again: presentation, really--think of it like CSS. Herein defines
the graphical counterpart to all aspects of the game which have one.

"""

import os
import glob
import render
import constants
import pyganim
import pygame
from PIL import Image
from collections import OrderedDict

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2015, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


class Animation(object):
    """I got sick of converting between pyganim, pygame, and PIL.

    Note:
      Currently no support for pygame_surfaces to pil_gif. a possible
      solution is seen below:

        http://svn.effbot.org/public/pil/Scripts/gifmaker.py

      It's not horribly handy to work with PIL once all the
      animations are assembled, anyway!

      I need to add support for creating from pygame surfaces, but
      that hasn't been necessary yet.

    Attibutes:
      pygame_surfaces (list):
      pyganim_gif (PygAnim):

    """

    def __init__(self, gif_path=None, pil_gif=None, pyganim_gif=None):
        """

        Args:
          gif_path (str|None): create animation using a path to a gif
          pil_gif (PIL.Image): create animation using a PIL Image()
          pyganim_gif (pyganim.PygAnimation): create animation using a
            PygAnimation object.

        """

        if gif_path:
            # open as PIL image
            pil_gif = Image.open(gif_path)

        if pil_gif:
            pygame_surfaces = self.pil_to_surfaces(pil_gif)
            pyganim_gif = pyganim.PygAnimation(pygame_surfaces)
            pyganim_gif.anchor(pyganim.CENTER)

        elif pyganim_gif:
            pygame_surfaces = self.pyganim_to_surfaces(pyganim_gif)

        self.pyganim_gif = pyganim_gif
        self.pygame_surfaces = pygame_surfaces

    def pyganim_to_surfaces(self, pyganim_gif):
        """Create a list of pygame surfaces with corresponding
        frame durations, from a PygAnimation.

        Args:
          pyganim_gif (pyganim.PygAnimation): extract the surfaces
            from this animation.

        Returns:
          list: a list of (pygame surface, frame duration) representing
            the frames from supplied pyganim_gif.

        """

        pygame_surfaces = zip(pyganim_gif._images, pyganim_gif._durations)

        return pygame_surfaces

    def pil_to_surfaces(self, pil_gif):
        """PIL Image() to list of pygame surfaces (surface, duration).

        Args:
          gif_path (str): GIF to open and load into a list
            of pygame surfaces.

        Returns:
          list: [(frame surface, duration), (frame, duration)]

        """

        frame_index = 0
        frames = []

        try:

            while 1:
                duration = pil_gif.info['duration'] / 1000.0
                frame_as_pygame_image = render.pil_to_pygame(pil_gif, "RGBA")
                frames.append((frame_as_pygame_image, duration))
                frame_index += 1
                pil_gif.seek(pil_gif.tell() + 1)

        except EOFError:

            pass # end of sequence

        return frames

    def get_max_size(self):
        """Boilerplate for consistency.

        Returns:
          tuple: (int x, int y) representing the pixel dimensions of
            the largest frame.

        """

        return self.pyganim_gif.getMaxSize()


class Walkabout(object):
    """Sprite animations for a character which walks around.

    Note:
      The walkabout sprites specified to be therein
      walkabout_directory, are files with an action__direction.gif
      filename convention.

      ASSUMPTION: walkabout_directory contains sprites for
      walk AND run actions.

    Attributes:
      animations (dict): --
      meta_animations (dict): --
      rect (pygame.Rect): --
      size (tuple): --
      action (constants.Action): --
      direction (constnts.Direction): --

    """

    def __init__(self, walkabout_directory='debug', start_position=None):
        """a description about reading animations from directory into
        object

        Args:
          walkabout_directory (str): directory containing (animated)
            walkabout GIFs. Assumed parent is data/walkabouts/
          start_position (tuple): (x, y) coordinates (integers)
            referring to absolute pixel coordinate.

        """

        # the attributes we're generating
        self.animations = {}
        self.meta_animations = {}
        self.size = None  # will be removed in future?

        # specify the files to load
        walkabout_directory = os.path.join(
                                           '../resources',
                                           'walkabouts',
                                           walkabout_directory
                                          )
        sprite_name_pattern = os.path.join(walkabout_directory, '*.gif')

        # get all the animations in this directory
        # what about if no sprites in directory? what if no such match?
        for sprite_path in glob.iglob(sprite_name_pattern):
            file_name, file_ext = os.path.splitext(sprite_path)
            file_name = os.path.split(file_name)[1]

            if file_name.startswith('meta_'):
                __, action, direction = file_name.split('_', 2)
                target = self.meta_animations
            else:
                action, direction = file_name.split('_', 1)
                target = self.animations

            direction = getattr(constants, direction.title())
            action = getattr(constants, action.title())

            animation = Animation(sprite_path)

            try:
                target[action][direction] = animation
            except KeyError:
                target[action] = {direction: animation}

        self.size = animation.get_max_size()
        position = start_position or (0, 0)  # px values

        # ... set the rest of the attribs
        self.rect = pygame.Rect(position, self.size)
        self.speed = 1
        self.action = constants.Stand
        self.direction = constants.Down

    def current_animation(self):

        return self.animations[self.action][self.direction]

    def equip(self, pygame_image):
        """Lazy, temporary method of visualy equipping items.

        Args:
          pygame_image (pygame.Surface): --

        """

        for action in (constants.Stand, constants.Walk):

            for direction in (constants.Up, constants.Down,
                              constants.Right, constants.Left):

                animation = self.animations[action][direction]
                meta_animation = self.meta_animations[action][direction]
                new_animation = render.anchor_to_animation(
                                                           animation,
                                                           meta_animation,
                                                           pygame_image
                                                          )
                self.animations[action][direction] = new_animation

        self.init()

    def blit(self, screen, offset):
        """Draw the appropriate/active animation to screen.

        Note:
          Should go to render module?

        Args:
          screen (pygame.Surface): the primary display/screen.
          offset (x, y tuple): the x, y coords of the absolute
            starting top left corner for the current screen/viewport
            position.

        """

        x, y = self.rect.topleft
        x -= offset[0]
        y -= offset[1]
        position_on_screen = (x, y)
        self.current_animation().pyganim_gif.blit(screen, position_on_screen)

    def init(self):
        actions = (constants.Walk, constants.Stand)
        directions = (constants.Up, constants.Down,
                      constants.Left, constants.Right)

        for action in actions:

            for direction in directions:
                animated_sprite = (self.animations[action][direction]
                                   .pyganim_gif)
                animated_sprite.convert_alpha()
                animated_sprite.convert()

                # this is me being lazy and impatient
                animated_sprite.play()


class Item(object):
    """An item on the ground which can be picked up.

    Note:
      An equipable item which has a sprite per side just
      uses Walkabout.

      Also: sprites don't have sounds! I'll later be adding
      an items.py.

    """

    def __init__(self, position, item_name='debug'):
        #self.game = game
        item_image_path = os.path.join(
                                       '../resources',
                                       'items',
                                       item_name + '.png'
                                      )
        item_image = pygame.image.load(item_image_path)
        self.size = item_image.get_size()
        self.image = item_image
        self.rect = pygame.Rect(position, self.size)
        self.position = position
        sound_path = os.path.join(
                                  '../resources',
                                  'sounds',
                                  'touch-fuzzy.wav'
                                 )
        self.pickup_sound =  pygame.mixer.Sound(sound_path)

    def blit(self, surface, viewport_offset=None):
        x, y = self.position
        x -= viewport_offset[0]
        y -= viewport_offset[1]
        position_on_screen = (x, y)
        surface.blit(self.image, position_on_screen)


class ExampleItem(Item):
    """Plays a sound and cycles the screen tint for a duration.

    Note:
      This has too manny features for a "sprite."

      Items role in the sprites module needs to be completely
      grounded in the graphical manipulation and presentation
      of items.

    """

    def pickup(self, player):
        self.pickup_sound.play()
        hat_image = '../resources/equipment/hat/mask_down.png'
        hat_image = pygame.image.load(hat_image)
        player.equip(hat_image)

        #if screen_effect:
        #    screen...

