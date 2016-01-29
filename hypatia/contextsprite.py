"""A sprite consisting of several sprites and whose current
sprite is resultant of its direction and action.

"""

import itertools

import pygame

from hypatia import animatedsprite


class NoContextForImage(Exception):
    """It is impossible to create a viable action/direction
    context from a file_name supplied which happens to have
    a file extension we consider to be an image.

    Attributes:
        file_name (str): The name of the file which was used
            to determine the action and direction, but failed.

    See Also:
        SpriteContexts
        InsufficientContexts

    """

    def __init__(self, file_name):
        self.file_name = file_name


class InsufficientContexts(Exception):
    """While attempting to create a ContextSprite,
    the minimum contexts were not fulfilled by
    whatever resource which supplies the sprites.

    Basically, not all of the action/direction
    combinations are present.

    Attributes:
        collection (any): the sequence of things
            which lacked the required contexts.

    """

    def __init__(self, collection):
        """

        Arguments:
            collection (?): the sequence of things
                which did not have enough contexts.

        """

        self.collection = collection


class SpriteContexts(object):
    """The action/direction to pygame Sprite mapping.

    """

    def __init__(self, sprite_contexts):
        """

        Args:
            sprite_contexts (dict): Keys are (action, direction)
                tuples (enumerations), values are of the
                pygame.Sprite type.

        """

        self.sprite_contexts = sprite_contexts

    @classmethod
    def from_files_dict(cls, files):
        """Take dictionary where key is the filename, and
        the values are either BytesIO or pygame.Sprite
        objects.

        Raises:
            NoContextForImage:
            InsufficientContexts:

        See Also:
            self.validate_dict()

        """

        valid_image_extensions = ("gif", "png")

        sprite_contexts = {}

        for file_name, file_data in files.items():
            file_name, file_ext = os.path.splitext(sprite_path)

            if file_ext not in valid_image_extensions:

                continue

            action, direction = file_name.split('_', 1)

            try:
                direction = getattr(constants.Direction, direction)
                action = getattr(constants.Action, action)

            except AttributeError:

                raise NoContextForImage(file_name)

            sprite_contexts[(action, direction)] = files[file_name]

        validate_dict(sprite_contexts)

    @staticmethod
    def validate_dict(sprite_contexts, also_ordinals=False):
        """Assure all of the direction/action contexts exist.

        Arguments:
            sprite_contexts (dict):
            also_ordinals (bool): If true, ordinals are required
                in addition to cardinal directions.

        Raises:
            InsufficientContexts:

        See Also:
            hypatia.constants: Action, Direction

        """

        if also_ordinals:
            directions = constants.Direction.cardinals_and_ordinals()
        else:
            directions = constants.Direction.cardinals()

        actions = constants.Action.all()

        for action, direction in itertools.product(actions, directions):

            try:
                sprite_contexts[(action, direction)]
            except KeyError:

                raise InsufficientContexts()


class ContextSprite(pygame.sprite.Sprite):
    """A sprite consisting of several sprites and whose current
    sprite is resultant of its current direction + action.

    Contains a mapping (dictionary) of current direction + action
    to pygame sprite (we call these "sprite contexts").

    Attributes:
        sprite_contexts (dict): Keys take the pattern of
            (action, direction) and values are the
            respective pygame sprites.
        image (pygame.Sprite): This is the current image/frame
            that was set by the update() method to reflect
            the current direction + action.
        animation (AnimatedSprite): Current animation which was
            set by the update() method to reflect the current
            direction + action.

    """

    def __init__(self, sprite_contexts, contextsprite_children=None,
                 absolute_position_float=None):

        super(Walkabout, self).__init__()

        self.sprite_contexts = {}
        self.contextsprite_children = None

        self.animation = None
        self.image = None

        self.direction = constants.Direction.south
        self.action = constants.Direction.south

        self.image = self.sprite_contexts[self.action][self.direction]

        self.absolute_position_float = absolute_position_float or (0.0, 0.0)

    @property
    def size(self):

        return self.image.get_size()

    @property
    def rect(self):

        return self.image.get_rect()

    def update(self, clock, viewport):
        """Call this once per main loop iteration (tick). Advance
        the active animation's frame according to the clock, use
        said surface/image/frame as this Walkabout's "image" attribute.

        Args:
            clock (pygame.time.Clock): The system clock. Typically
                and defaultly the game.screen.clock. It will control
                the animation. Time is a key factor in updating the
                animations.

        See Also:
            * animatedsprite.AnimatedSprite
            * animatedsprite.AnimatedSprite.update()
            * pygame.time.Clock

        """

        self.animation = self.image_contexts[self.action][self.direction]
        self.animation.update(clock
                              self.topleft_float,
                              viewport)
        self.image = self.animation.image

    def blit(self, clock, viewport):
        """Draw the appropriate/active animation to screen.

        Args:
            clock (pygame.time.Clock): The system clock. Typically
                and defaultly the game.screen.clock. It will control
                the animation. Time is a key factor in updating the
                animations.

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
        x, y = self.absolute_position_float
        x -= offset[0]
        y -= offset[1]
        # sprite position on viewport
        # There are no half-pixels, thus we don't use floats.
        position_on_screen = (int(x), int(y))

        # Update the state of the current animation. This affects
        # this Walkabout's `image` property.
        self.update(clock, viewport)

        # Blit the current image for this Walkabout to the
        # supplied viewport surface (`screen`) at the supplied
        # `position_on_screen`, which we figured out earlier.
        viewport.blit(self.image, self.absolute_position_float)

        # Render and update child walkabouts. Render a child
        # Walkabout so that its head anchor occupies the same
        # position as its parent head anchor (THIS Walkabout).
        #
        # This means getting the difference between the following
        # child anchors and THIS Walkabout's (parent) anchors and
        # using said difference as the offset for the child
        # Walkabout sprite/animation.
        current_frame = self.animation..active_frame
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
            child_active_anim = child_walkabout.animation
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

    def optimize(self):
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

        for child in self.children:
            child.optimize()
