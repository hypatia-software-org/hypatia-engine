# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""Sprites!

Tools for animation. Animation sources are GIFs from disk, which
have been made into an AnimatedSprite object. Stateful animations
which represent objects, e.g., :class:`Walkabout` represents an
:class:`actor.Actor`.

Examples of "tools":

  * functions for creating an animation from a single suface
  * loading animations from disk
  * adding frame-specific positional data
  * contextually-aware sprites

Warning:
    Sometimes an "animation" can consist of one frame.

Note:
    I wanna add support for loading character animations
    from sprite sheets.

See Also:

    * :mod:`resources`
    * :mod:`actor`
    * :class:`Walkabout`

"""

import os
import copy
import itertools
import collections

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

import pygame
from PIL import Image

from hypatia import constants
from hypatia import resources
from hypatia import animatedsprite


class BadWalkabout(Exception):
    """Walkabout Resource specified does not contain any
    GIF files (AnimatedSprite) for creating a Walkabout sprite.

    Used in Walkabout when no files match "*.gif"
    in the provided Resource.

    Attributes:
        failed_name (str): The supplied archive was appended to the
            resources' walkabout direction. This is the value of
            the attempted which resulted in KeyError.

    See Also:
        * Walkabout.__init__()
        * resources.Resource

    """

    def __init__(self, failed_name):
        """Set the exception message and "failed_name" attribute
        to the provided failed_name argument.

        Args:
            failed_name (str): :class:`Walkabout` resource archive
                which *should* have contained files of pattern
                ``*.gif,`` but didn't.

        """

        super(BadWalkabout, self).__init__(failed_name)
        self.failed_name = failed_name


class Walkabout(pygame.sprite.Sprite):
    """Sprite animations for a character which walks around.

    Contextually-aware graphical representation.

    The walkabout sprites specified to be therein
    walkabout_directory, are files with an action__direction.gif
    filename convention.

    Blits its children relative to its own anchor.

    Attributes:
        resource (Resource): --
        animations (dict): 2D dictionary [action][direction] whose
            values are PygAnimations.
        animation_anchors (dict): 2D dictionary [action][direction]
            whose values are AnimAnchors.
        rect (pygame.Rect): position on tilemap
        size (tuple): the size of the animation in pixels.
        action (constants.Action): --
        direction (constnts.Direction): --
        topleft_float (x,y tuple): --
        position_rect

    """

    def __init__(self, directory, position=None, children=None):
        """

        Args:
            directory (str): directory containing (animated)
            walkabout GIFs. Assumed parent is data/walkabouts/
            position (tuple): (x, y) coordinates (integers)
                referring to absolute pixel coordinate.
            children (list|None): Walkabout objects drawn relative to
                this Walkabout instance.

        Example:
            >>> hat = Walkabout('hat')
            >>> Walkabout('debug', position=(44, 55), children=[hat])
            <Walkabout sprite(in ... groups)>

        """

        super(Walkabout, self).__init__()

        # the attributes we're generating
        self.animations = {}
        self.animation_anchors = {}
        self.actions = []
        self.directions = []
        self.size = None  # will be removed in future?

        if not position:
            position = (0, 0)

        topleft_float = (float(position[0]), float(position[1]))

        # specify the files to load
        # how will i glob a resource
        resource = resources.Resource('walkabouts', directory)
        sprite_files = resource.get_type('.gif')

        # no sprites matching pattern!
        if not sprite_files:

            raise BadWalkabout(directory)

        for sprite_path in sprite_files.keys():
            file_name, file_ext = os.path.splitext(sprite_path)
            file_name = os.path.split(file_name)[1]

            if file_name == 'only':
                action = constants.Action.stand
                direction = constants.Direction.south

            else:
                action, direction = file_name.split('_', 1)
                direction = getattr(constants.Direction, direction)
                action = getattr(constants.Action, action)

            self.actions.append(action)
            self.directions.append(direction)

            # load pyganim from gif file
            animation = sprite_files[sprite_path]

            try:
                self.animations[action][direction] = animation
            except KeyError:
                self.animations[action] = {direction: animation}

        # ... set the rest of the attribs
        self.resource = resource

        # NOTE: this is lazy and results in smaller frames
        # having a bunch of "padding"
        self.size = animation.largest_frame_size()

        self.rect = pygame.Rect(position, self.size)
        self.topleft_float = topleft_float
        self.action = constants.Action.stand
        self.direction = constants.Direction.south
        self.child_walkabouts = children or []

        self.image = self.animations[self.action][self.direction]

    def __getitem__(self, key):
        """Fetch sprites associated with action (key).

        Args:
            key (constants.Action): return dictionary of
                sprites for this action (key).

        Returns:
            dict: sprites associated with action supplied (key)

        Examples:
            >>> walkabout = Walkabout('debug')
            >>> walkabout[constants.Action.walk][constants.Direction.south]
            <AnimatedSprite sprite(in ... groups)>

        """

        return self.animations[key]

    def current_animation(self):
        """Returns the animation selected by the current action
        and direction.

        Returns:
            PygAnim: the animation associated with this Walkabout's
                current action and direction.

        Example:
            >>> walkabout = Walkabout('debug')
            >>> walkabout.current_animation()
            <AnimatedSprite sprite(in ... groups)>

        """

        return self.animations[self.action][self.direction]

    def update(self, clock, screen, offset):
        """Call this once per main loop iteration (tick). Advance
        the active animation's frame according to the clock, use
        said surface/image/frame as this Walkabout's "image" attribute.

        Args:
            clock (pygame.time.Clock): The system clock. Typically
                and defaultly the game.screen.clock. It will control
                the animation. Time is a key factor in updating the
                animations.
            screen (???): I think I'm actually sending the
                viewport, here, I'm not sure? Will touch up later.

        See Also:
            * Walkabout.current_animation()
            * animatedsprite.AnimatedSprite
            * pygame.time.Clock

        """

        active_animation = self.current_animation()
        active_animation.update(clock,
                                self.topleft_float,
                                screen)
        self.image = active_animation

    def blit(self, clock, screen, offset):
        """Draw the appropriate/active animation to screen.

        Args:
            screen (pygame.Surface): the primary display/screen.
            offset (x, y tuple): the x, y coords of the absolute
                starting top left corner for the current
                screen/viewport position.
            clock (pygame.time.Clock): The system clock. Typically
                and defaultly the game.screen.clock. It will control
                the animation. Time is a key factor in updating the
                animations.

        """

        x, y = self.topleft_float
        x -= offset[0]
        y -= offset[1]
        position_on_screen = (x, y)

        self.update(clock, screen, offset)
        current_frame = self.current_animation().active_frame()
        screen.blit(current_frame.surface, position_on_screen)
        animation_anchors = current_frame.anchors
        # we do this because currently the only
        # applicable anchor is head
        frame_anchor = animation_anchors['head_anchor']

        # outdated method, but using for now...
        parent_anchor_x = position_on_screen[0] + frame_anchor.x
        parent_anchor_y = position_on_screen[1] + frame_anchor.y
        parent_anchor = animatedsprite.Anchor(parent_anchor_x,
                                              parent_anchor_y)

        for child_walkabout in self.child_walkabouts:
            # draw at position + difference in child anchor
            child_active_anim = child_walkabout.current_animation()
            child_active_anim.update(clock,
                                     self.topleft_float,
                                     screen)
            child_active_frame = child_active_anim.active_frame()
            child_frame_anchor = child_active_frame.anchors['head_anchor']
            child_position = (parent_anchor - child_frame_anchor).as_tuple()
            screen.blit(child_active_anim.image, child_position)

    def runtime_setup(self):
        """Perform actions to setup the walkabout. Actions performed
        once pygame is running and walkabout has been initialized.

        Convert and play all the animations, run init for children.

        Note:
            It MAY be bad to leave the sprites in play mode in startup
            by default.

        """

        if len(self.animations) == 1:
            actions = (constants.Action.stand,)
            directions = (constants.Direction.south,)

        else:
            actions = (constants.Action.walk, constants.Action.stand)
            directions = (constants.Direction.north, constants.Direction.south,
                          constants.Direction.east, constants.Direction.west)

        for action in actions:

            for direction in directions:
                animated_sprite = self.animations[action][direction]
                animated_sprite.convert_alpha()

        for walkabout_child in self.child_walkabouts:
            walkabout_child.runtime_setup()


def palette_cycle(surface):
    """get_palette is not sufficient; it generates superflous colors.

    Note:
      Need to see if I can convert 32bit alpha to 8 bit temporarily,
      to be converted back at end of palette/color manipulations.

    """

    original_surface = surface.copy()  # don't touch! used for later calc
    width, height = surface.get_size()
    ordered_color_list = []
    seen_colors = set()

    for coordinate in itertools.product(range(0, width), range(0, height)):
        color = surface.get_at(coordinate)
        color = tuple(color)

        if color in seen_colors:

            continue

        ordered_color_list.append(color)
        seen_colors.add(color)

    # reverse the color list but not the pixel arrays, then replace!
    old_color_list = collections.deque(ordered_color_list)
    new_surface = surface.copy()
    frames = []

    for rotation_i in range(len(ordered_color_list)):
        new_surface = new_surface.copy()

        new_color_list = copy.copy(old_color_list)
        new_color_list.rotate(1)

        color_translations = dict(zip(old_color_list, new_color_list))

        # replace each former color with the color from newcolor_list
        for coordinate in itertools.product(range(0, width), range(0, height)):
            color = new_surface.get_at(coordinate)
            color = tuple(color)
            new_color = color_translations[color]
            new_surface.set_at(coordinate, new_color)

        frame = new_surface.copy()
        frames.append((frame, 250))
        old_color_list = copy.copy(new_color_list)

    return animatedsprite.AnimatedSprite.from_surface_duration_list(frames)
