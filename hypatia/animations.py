# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""Tools for animation. Animation sources are GIFs from disk, which
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

    * :mod:`util`
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
import pyganim
from PIL import Image

from hypatia import util
from hypatia import constants


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
        * util.Resource

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


class AnimAnchors(object):
    """The anchors per frame of a :class:`pyganim.PygAnimation`. Anchors
    are coordinates belonging to a :class:`pygame.Surface`, which can be
    translated to coordinates belonging to another surface.

    With :class:`AnimAnchors` you can keep one animation "pinned" or
    "glued" to another. This can help with adding decals to a
    :class;`Walkabout` animation (like a hat!).

    Attributes:
        anchor_points (dict): key is anchor label/group, value is a list
            of :class:`AnchorPoint` instances whose index corresponds to
            respective :class:`pyganim.PygAnimation` frame index.
        anchor_groups (list): the names/labels of the anchor groups,
            e.g., *head_anchor*.

    Example:
        >>> resource = util.Resource('walkabouts', 'debug')
        >>> anchors = AnimAnchors.from_config(resource['walk_north.ini'])
        >>> anchors.anchor_points['head_anchor']
        [<hypatia.animations.AnchorPoint object at 0x...>, ...]
        >>> anchors.anchor_groups
        ['head_anchor']

    Note:
        You can modify anchors--there's no reason they have to be
        immutable. You can even build them yourself. Remember the
        tall cacti from Mario? How about a spinning mace?

    See Also:

        * :class:`AnchorPoint`
        * :meth:`Walkabout.blit`

    """

    def __init__(self, anchor_points, anchor_groups):
        self.anchor_points = anchor_points
        self.anchor_groups = anchor_groups

    @classmethod
    def from_config(cls, anchor_ini):
        """Instantiate AnimAnchors using the anchor_ini config.

        The anchor_ini derives from an INI like this:

            [head_anchor]
            0=0,2
            1=1,3
            2=2,2

        `[head_anchor]` is the anchor label. The stuff below it is
        `head_anchor`'s position for frames 0, 1, and 2.

        In the above example, `head_anchor` has a coordinate (anchor)
        for three different frames:

        * frame 0 at (0, 2)
        * frame 1 at (1, 3)
        * frame 2 at (2, 2)

        Note:
            `anchor_ini` should be provided from a
            :class:`util.Resource`. See example below.

        Args:
            anchor_ini (configparser): configparser object.

        Example:
            >>> resource = util.Resource('walkabouts', 'debug')
            >>> AnimAnchors.from_config(resource['walk_north.ini'])
            <hypatia.animations.AnimAnchors object at 0x...>

        Returns:
            AnimAnchors: anchor points and groups collected from an INI

        """

        anchor_point_groups = anchor_ini.sections()

        # key is group, value is list of frame coord positions
        anchors = {name: [] for name in anchor_point_groups}

        for anchor_point_group in anchor_point_groups:

            for __, frame_anchor in anchor_ini.items(anchor_point_group):
                x, y = frame_anchor.split(',')
                anchor_point = AnchorPoint(int(x), int(y))
                anchors[anchor_point_group].append(anchor_point)

        return AnimAnchors(anchors, anchor_point_groups)

    def get_anchor_point(self, anchor_point_group, frame_index):
        """Return an :class:`AnchorPoint` corresponding to group name
        and frame index.

        Args:
            anchor_point_group (str): name of the anchor point group
            frame_index (int): which frame for group's anchor

        Returns:
            AnchorPoint: --

        Note:
            Will simply return last anchor point for group if an anchor
            isn't defined for frame.

        Example:
            >>> resource = util.Resource('walkabouts', 'debug')
            >>> config = resource['walk_north.ini']
            >>> animation_anchors = AnimAnchors.from_config(config)
            >>> animation_anchors.get_anchor_point('head_anchor', 0)
            <hypatia.animations.AnchorPoint object at 0x...>

        """

        try:

            return self.anchor_points[anchor_point_group][frame_index]

        except IndexError:

            return self.anchor_points[anchor_point_group][-1]


class AnchorPoint(object):
    """A coordinate on a surface which is used for pinning to another
    surface AnchorPoint. Used when attempting to afix one surface to
    another, lining up their corresponding anchorpoints.

    Attributes:
        x (int): x-axis coordinate on a surface to place anchor at
        y (int): x-axis coordinate on a surface to place anchor at

    """

    def __init__(self, x, y):
        """Create an AnchorPoint at coordinate (x, y).

        Args:
            x (int): the x-axis pixel position
            y (int): the y-axis pixel position

        Example:
            >>> anchor_point = AnchorPoint(5, 3)
            >>> anchor_point.x
            5
            >>> anchor_point.y
            3

        """

        self.x = x
        self.y = y

    def __add__(self, other_anchor_point):
        """Adds the x, y values of this and another anchor point.

        Args:
            other_anchor_point (AnchorPoint): the AnchorPoint
                coordinates to add to this AnchorPoint's coordinates.

        Returns:
            (x, y) tuple: the new x, y coordinate

        Example:
            >>> anchor_point_a = AnchorPoint(4, 1)
            >>> anchor_point_b = AnchorPoint(2, 0)
            >>> anchor_point_a + anchor_point_b
            (6, 1)

        """

        return (self.x + other_anchor_point.x,
                self.y + other_anchor_point.y)

    def __sub__(self, other_anchor_point):
        """Find the difference between this anchor and another.

        Args:
            other_anchor_point (AnchorPoint): the AnchorPoint
                coordinates to subtract from this
                AnchorPoint's coordinates.

        Returns:
            tuple: the (x, y) difference between this
                anchor point and the other supplied.

        Example:
            >>> anchor_point_a = AnchorPoint(4, 1)
            >>> anchor_point_b = AnchorPoint(2, 0)
            >>> anchor_point_a - anchor_point_b
            (2, 1)

        """

        return (self.x - other_anchor_point.x,
                self.y - other_anchor_point.y)


# NOTE: this will eventually be replaced with a much more
# sophisicated version, as seen in the EVERYTHING-CHANGES
# branch. Right now I am trying to implement AnimatedSprite
# with as little changes as possible.
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
        resource = util.Resource('walkabouts', directory)
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

            # NOTE: commented out, because now when GIFs are
            # loaded into AnimatedSprite objects, they have
            # their anchor points defined in frame objects.
            """
            # load anchor points
            # erro here not loading all the time
            # maybe make the ini exlpicit? this caused porbs
            associated_ini_name = file_name + '.ini'

            if associated_ini_name in resource:
                anchors_ini = resource[associated_ini_name]
                anim_anchors = AnimAnchors.from_config(anchors_ini)

                try:
                    self.animation_anchors[action][direction] = anim_anchors
                except KeyError:
                    self.animation_anchors[action] = {direction: anim_anchors}

            else:
                self.animation_anchors = None
            """
            # ... thus we have to hackily set the
            # self.animation_anchors object using the anchor data from
            # the frames consisting the AnimatedSprite object.
            #
            # if first frame has anchor, presume rest do and set
            # self.animation_anchors based on this, else set to None.
            if animation.frames[0].anchors:
                animation_anchors = {}

                for frame in animation.frames:

                    try:
                        animation_anchors[action][direction] = frame.anchors
                    except KeyError:
                        animation_anchors[action] = {direction: frame.anchors}

                self.animation_anchors = animation_anchors

            else:
                self.animation_anchors = None

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

    def get_anchors(self):
        """Get anchors per frame in a GIF by identifying th ecoordinate
        of a specific color.

        Warning:
            This is an old, but still useful way of loading anchors for
            an animation.

        """

        anchors = {a: {d: [] for d in self.directions} for a in self.actions}

        for action, directions in self.animations.items():

            for direction, animation in directions.items():

                for surface_frame in animation._images:
                    anchor = self.get_anchor(surface_frame)
                    anchors[action][direction].append(anchor)

        return anchors

    def get_anchor(self, surface):
        """Locate the anchor coordinate by identifying which pixel
        coordinate matches color.

        Args:
            surface (pygame.Surface): surface to scan for color and
                return the coord which color appears

        Returns:
            tuple: (x, y) pixel coordinate where color shows up.

        Warning:
            Old way of defining anchor points, but still handy!

        """

        x, y = surface.get_size()
        debug_color = pygame.Color(255, 136, 255)

        for coord in itertools.product(range(0, x), range(0, y)):

            if surface.get_at(coord) == debug_color:

                return coord

    def update(self, clock, screen, offset):
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
              starting top left corner for the current screen/viewport
              position.

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
        parent_anchor = AnchorPoint(position_on_screen[0] + frame_anchor.x,
                                    position_on_screen[1] + frame_anchor.y)

        for child_walkabout in self.child_walkabouts:
            # draw at position + difference in child anchor
            child_active_anim = child_walkabout.current_animation()
            child_active_anim.update(clock,
                                     self.topleft_float,
                                     screen)
            child_active_frame = child_active_anim.active_frame()
            child_frame_anchor = child_active_frame.anchors['head_anchor']
            child_position = parent_anchor - child_frame_anchor
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
        frames.append((frame, 0.2))
        old_color_list = copy.copy(new_color_list)

    return pyganim.PygAnimation(frames)
