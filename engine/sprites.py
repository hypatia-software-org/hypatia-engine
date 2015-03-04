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


class BadWalkabout(Exception):
    """The supplied directory has no files which match *.gif.

    """

    def __init__(self, supplied_directory):
        super(BadWalkabout, self).__init__(supplied_directory)


class Animation(object):
    """Animation abstraction of animation gif and its respective
    meta animation gif.

    Attibutes:
      gif (pyganim.PygAnimation): --
      meta_gif (pyganim.PygAnimation): --

    """

    def __init__(self, gif_path):
        """Load gif_path to PygAnimation, as well as respective
        meta gif.

        Args:
          gif_path (str|None): create animation using a path to a gif

        """

        # create path for meta gif
        gif_dir, gif_name = os.path.split(gif_path)
        meta_gif_name = "meta_" + gif_name
        meta_gif_path = os.path.join(gif_dir, meta_gif_name)

        # set attributes
        self.gif = self.pyganim_from_path(gif_path)
        self.meta_gif = self.pyganim_from_path(meta_gif_path)

    def pyganim_from_path(self, gif_path):
        """Create a PygAnimation utilizing the GIF animation specified
        in gif_path.

        Args:
          gif_path (str): path to GIF.

        Returns:
          pyganim.PygAnimation: comprised of the times and frames from
            specified GIF.

        """

        pil_gif = Image.open(gif_path)

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

        gif = pyganim.PygAnimation(frames)
        gif.anchor(pyganim.CENTER)

        return gif

    def get_max_size(self):
        """Boilerplate for consistency.

        Returns:
          tuple: (int x, int y) representing the pixel dimensions of
            the largest frame.

        """

        return self.gif.getMaxSize()


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
      animations (dict): 2D dictionary [action][direction] whose
        values are PygAnimations.
      rect (pygame.Rect): position on tilemap
      size (tuple): the size of the animation in pixels.
      action (constants.Action): --
      direction (constnts.Direction): --
      topleft_float (x,y tuple): --

    """

    def __init__(self, directory='debug', position=None, children=None):
        """

        Args:
          directory (str): directory containing (animated)
            walkabout GIFs. Assumed parent is data/walkabouts/
          position (tuple): (x, y) coordinates (integers)
            referring to absolute pixel coordinate.
          children (list|None): Walkabout objects drawn relative to
            this Walkabout instance.

        """

        # the attributes we're generating
        self.animations = {}
        self.actions = []
        self.directions = []
        self.size = None  # will be removed in future?
        
        if not position:
            position = (0, 0)

        topleft_float = (float(position[0]), float(position[1]))

        # specify the files to load
        walkabout_directory = os.path.join(
                                           '../resources',
                                           'walkabouts',
                                           directory
                                          )
        sprite_name_pattern = os.path.join(walkabout_directory, '*.gif')

        # get all the animations in this directory
        # what about if no sprites in directory? what if no such match?
        sprite_paths = glob.glob(sprite_name_pattern)

        if not sprite_paths:

            raise BadWalkabout(directory)

        for sprite_path in sprite_paths:
            file_name, file_ext = os.path.splitext(sprite_path)
            file_name = os.path.split(file_name)[1]

            # we do this because Animation handles meta_
            if file_name.startswith('meta_'):

                continue

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

        # ... set the rest of the attribs
        self.size = animation.get_max_size()
        self.rect = pygame.Rect(position, self.size)
        self.topleft_float = topleft_float
        self.action = constants.Stand
        self.direction = constants.Down
        self.speed_in_pixels_per_second = 20.0
        self.child_walkabouts = children or []
        self.anchors = self.get_anchors()
        
        self.init()

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

    def current_animation(self):
        """Returns the animation selected by the current action
        and direction.

        """

        return self.animations[self.action][self.direction]

    def get_anchors(self):
        """needs to get actual offset"""

        anchors = {a: {d: [] for d in self.directions} for a in self.actions}

        for action, directions in self.animations.items():

            for direction, animation in directions.items():
                meta_gif = animation.meta_gif

                for surface_frame in meta_gif._images:
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

        pyganim_gif = self.current_animation().gif
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
            child_pyganim = child_walkabout.current_animation().gif
            child_pyganim.blit(screen, child_position)

    def init(self):
        actions = (constants.Walk, constants.Stand)
        directions = (constants.Up, constants.Down,
                      constants.Left, constants.Right)

        for action in actions:

            for direction in directions:
                animated_sprite = self.animations[action][direction].gif
                animated_sprite.convert_alpha()
                animated_sprite.convert()

                # this is me being lazy and impatient
                animated_sprite.play()

        for walkabout_child in self.child_walkabouts:
            walkabout_child.init()
