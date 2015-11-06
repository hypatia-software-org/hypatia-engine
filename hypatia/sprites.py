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

    See Also:
        * actor.Actor: The Walkabout class represents an
        actor object!

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
            >>> debug = Walkabout('debug')
            >>> Walkabout('debug', position=(44, 55), children=[debug])
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

        # If the last file_name from the above for loop is "only,"
        # that means that that name denotes the fact that there is
        # ONLY one sprite for the supplied Walkabout resource.
        if file_name == 'only':

            # We want to set all the appropriate action/direction
            # animations in the self.animations dictionary to the
            # only animation provided, which was assigned as the
            # "Stand South" animation.
            animation = (self.animations[constants.Action.stand][
                         constants.Direction.south])

            for action in constants.Action.all():

                for direction in constants.Direction.cardinals_and_ordinals():

                    # We set everything to the Stand South animation since
                    # it was set first.
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
            * animatedsprite.AnimatedSprite.update()
            * pygame.time.Clock

        """

        active_animation = self.current_animation()
        active_animation.update(clock,
                                self.topleft_float,
                                screen)
        self.image = active_animation.image

    def blit(self, clock, screen, offset):
        """Draw the appropriate/active animation to screen.

        Args:
            clock (pygame.time.Clock): The system clock. Typically
                and defaultly the game.screen.clock. It will control
                the animation. Time is a key factor in updating the
                animations.
            screen (pygame.Surface): the primary display/screen.
            offset (x, y tuple): the x, y coords of the absolute
                starting top left corner for the current
                screen/viewport position.

        Note:
            All sprites will be sync'd because of how clock
            ticks work. The clock is ticked once per main
            loop iteration, and animations are advanced by
            getting the difference between two ticks.

        """

        # `position_on_screen` is the Walkabout sprite's
        # position ON SCREEN.
        #
        # `position_on_screen` is derived from the absolute
        # position of this Walkabout, i.e., the `topleft_float`
        # attribute, being subtracted by the provided `offset`.
        x, y = self.topleft_float
        x -= offset[0]
        y -= offset[1]
        # sprite position on viewport
        # There are no half-pixels, thus we don't use floats.
        position_on_screen = (int(x), int(y))

        # Update the state of the current animation. This affects
        # this Walkabout's `image` property.
        #
        # See: Walkabout.update()
        self.update(clock, screen, offset)

        # Blit the current image for this Walkabout to the
        # supplied viewport surface (`screen`) at the supplied
        # `position_on_screen`, which we figured out earlier.
        screen.blit(self.image, position_on_screen)

        # Render and update child walkabouts. Render a child
        # Walkabout so that its head anchor occupies the same
        # position as its parent head anchor (THIS Walkabout).
        #
        # This means getting the difference between the following
        # child anchors and THIS Walkabout's (parent) anchors and
        # using said difference as the offset for the child
        # Walkabout sprite/animation.
        current_frame = self.current_animation().active_frame
        parent_anchor = current_frame.anchors['head_anchor']
        # Adjust the parent anchor to consider the
        # position on screen for child walkabout
        # anchor calculations.
        parent_anchor = parent_anchor + position_on_screen

        for child_walkabout in self.child_walkabouts:
            # We update the current animation to reflect this
            # Walkabout's current action and direction.
            child_walkabout.action = self.action
            child_walkabout.direction = self.direction

            # Get and update this child walkabout's
            # current animation.
            child_active_anim = child_walkabout.current_animation()
            child_active_anim.update(clock,
                                     self.topleft_float,
                                     screen)

            # Now that the child walkabout's current animation
            # has been updated, get the active frame of the
            # child animation in order to find its head anchor.
            child_active_frame = child_active_anim.active_frame
            child_frame_anchor = child_active_frame.anchors['head_anchor']

            # As aforementioned, resolve the child Walkabout's
            # position by subtracting the child's anchor from
            # the adjusted parent anchor.
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
