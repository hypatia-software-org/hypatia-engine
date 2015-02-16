# engine/sprites.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia Engine and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""The stuff being drawn; sprites

"""

import os
import glob
import itertools
from collections import OrderedDict

import pyganim
import pygame
from PIL import Image

import render
import constants

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

      Blits its children relative to its own anchor.

    Attributes:
      animations (dict): --
      meta_animations (dict): --
      rect (pygame.Rect): --
      size (tuple): --
      action (constants.Action): --
      direction (constnts.Direction): --
      topleft_float (x,y tuple): --

    """

    def __init__(self, walkabout_directory='debug', start_position=None,
                 children=None):
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
        self.actions = []
        self.directions = []
        self.size = None  # will be removed in future?
        self.topleft_float = (0.0, 0.0)

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

            self.actions.append(action)
            self.directions.append(direction)

            animation = Animation(sprite_path)

            try:
                target[action][direction] = animation
            except KeyError:
                target[action] = {direction: animation}

        position = start_position or (0, 0)  # px values

        # ... set the rest of the attribs
        self.size = animation.get_max_size()
        self.rect = pygame.Rect(position, self.size)
        self.topleft_float = (0.0, 0.0)  # what if position is offered
        self.action = constants.Stand
        self.direction = constants.Down
        self.speed_in_pixels_per_second = 20.0
        self.child_walkabouts = children or []
        self.anchors = self.get_anchors()

    def __getitem__(self, key):
        """Fetch sprites associated with action (key).

        Args:
          key (constants.Action): return dictionary of sprites for
            this action (key).

        Returns:
          dict: sprites associated with action supplied (key)

        Examples:
          >>> walkabout = Walkabout()
          >>> walkabout[constants.Walk][constants.Up]
          <Animation Object>

        """

        return self.animations[key]

    def current_animation(self, meta=False):
        """Returns the animation selected by the current action
        and direction.

        """

        if meta:

            return self.meta_animations[self.action][self.direction]

        else:

            return self.animations[self.action][self.direction]

    def get_anchors(self):
        """needs to get actual offset"""

        anchors = {a: {d: [] for d in self.directions} for a in self.actions}

        for action, directions in self.meta_animations.items():

            for direction, animation in directions.items():

                for surface_frame in animation.pyganim_gif._images:
                    anchor = self.get_anchor(surface_frame)
                    anchors[action][direction].append(anchor)

        return anchors

    def get_anchor(self, surface):
        x, y = surface.get_size()
        debug_color = pygame.Color(255, 136, 255)

        for coord in itertools.product(range(0, x), range(0, y)):

            if surface.get_at(coord) == debug_color:

                return coord

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

        x, y = self.topleft_float
        x -= offset[0]
        y -= offset[1]
        position_on_screen = (x, y)

        pyganim_gif = self.current_animation().pyganim_gif
        pyganim_gif.blit(screen, position_on_screen)

        pyganim_frame_index = pyganim.findStartTime(pyganim_gif._startTimes,
                                                    pyganim_gif.elapsed)
        current_frame_surface = pyganim_gif.getFrame(pyganim_frame_index)

        animation_anchors = self.anchors[self.action][self.direction]
        frame_anchor = animation_anchors[pyganim_frame_index]  # use as offset
        parent_anchor_position = (position_on_screen[0] + frame_anchor[0],
                                  position_on_screen[1] + frame_anchor[1])

        for child_walkabout in self.child_walkabouts:
            # draw at positition + difference in child anchor
            child_anchor = (child_walkabout
                            .anchors[self.action][self.direction][0])  # lazy/testing
            child_position = (parent_anchor_position[0] - child_anchor[0],
                              parent_anchor_position[1] - child_anchor[1])
            child_pyganim = child_walkabout.current_animation().pyganim_gif
            child_pyganim.blit(screen, child_position)

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

        for walkabout_child in self.child_walkabouts:
            walkabout_child.init()

