"""Quite specifically my pyganim replacement.

More advanced animation/sprite abstractions are in
the animations module.

"""

import pygame
from PIL import Image


class Anchor(object):
    """A coordinate on a surface which is used for pinning to another
    surface Anchor. Used when attempting to afix one surface to
    another, lining up their corresponding anchors.

    Attributes:
        x (int): x-axis coordinate on a surface to place anchor at
        y (int): x-axis coordinate on a surface to place anchor at

    Example:
        >>> anchor = Anchor(5, 3)
        >>> anchor.x
        5
        >>> anchor.y
        3

    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):

        return "<Anchor at (%d, %d)>" % (self.x, self.y)

    def __add__(self, other_anchor):
        """Adds the x, y values of this and another anchor.

        Args:
            other_anchor (Anchor): The Anchor coordinates
                to add to this Anchor's coordinates.

        Returns:
            (x, y) tuple: the new x, y coordinate

        Example:
            >>> anchor_a = Anchor(4, 1)
            >>> anchor_b = Anchor(2, 0)
            >>> anchor_a + anchor_b
            <Anchor at (6, 1)>

        """

        return Anchor(self.x + other_anchor.x,
                      self.y + other_anchor.y)

    def __sub__(self, other_anchor):
        """Find the difference between this anchor and another.

        Args:
            other_anchor (Anchor): the Anchor
                coordinates to subtract from this
                AnchorPoint's coordinates.

        Returns:
            tuple: the (x, y) difference between this
                anchor and the other supplied.

        Example:
            >>> anchor_a = Anchor(4, 1)
            >>> anchor_b = Anchor(2, 0)
            >>> anchor_a - anchor_b
            <Anchor at (2, 1)>

        """

        return Anchor(self.x - other_anchor.x,
                      self.y - other_anchor.y)


class LabeledSurfaceAnchors(object):
    """Labeled anchors for a surface.

    """

    def __init__(self, anchors_config, frame_index):
        """The default is to simply load the anchors from
        the GIF's anchor config file.

        Args:
            anchors_config (resources?): --
            frame_index (int): Which animation frame do the
                anchors belong to?

        Raises:
            KeyError: INI has no anchor entry for frame_index.
            ValueError: INI's corresponding anchor entry is
                malformed.

        """

        self._labeled_anchors = {}

        for section in anchors_config.sections():
            anchor_for_frame = anchors_config.get(section, str(frame_index))
            x, y = anchor_for_frame.split(',')
            self._labeled_anchors[section] = Anchor(int(x), int(y))

    def __getitem__(self, label):
        """Return the anchor corresponding to label.

        Raises:
            KeyError: label does not correspond to anything.

        """

        return self._labeled_anchors[label]


class AnimatedSpriteFrame(object):
    """A frame of an AnimatedSprite animation.

    Attributes:
        surface (pygame.Surface): The pygame image which is used
            for a frame of an animation.
        duration (integer): Milliseconds this frame lasts. How
            long this frame is displayed in corresponding animation.
            The default is 0.
        start_time (integer): The millesecond in which this frame
            will be displayed. The default is 0.
        anchors (LabeledSurfaceAnchors): Optional positional anchors
            used when afixing other surfaces upon another.

    See Also:
        :method:`AnimatedSprite.frames_from_gif()`

    """

    def __init__(self, surface, start_time, duration, anchors=None):
        """

        Args:
            surface (pygame.Surface): The surface/image for this
                frame.
            duration (integer): Milleseconds this frame lasts.
            anchors (LabeledSurfaceAnchors): --

        """

        self.surface = surface
        self.duration = duration
        self.start_time = start_time
        self.end_time = start_time + duration
        self.anchors = anchors or None

    def __repr__(self):
        s = "<AnimatedSpriteFrame duration(%s) start_time(%s) end_time(%s)>"

        return s % (self.duration, self.start_time, self.end_time)


class AnimatedSprite(pygame.sprite.Sprite):
    """Animated sprite with mask, loaded from GIF.

    Supposed to be mostly uniform with the Sprite API.

    Notes:
        This is replacing pyganim as a dependency. Currently,
        does not seem to draw. I assume this is a timedelta
        or blending problem. In elaboration, this could also
        be related to the fact that sprites are rendered
        one-at-a-time, but they SHOULD be rendered through
        sprite groups.

        The rect attribute is useless; should not be used,
        should currently be avoided. This is a problem
        for animated tiles...

    Attributes:
        total_duration (int): The total duration of of this
            animation in milliseconds.
        image (pygame.Surface): Current surface belonging to
            the active frame.
        rect (pygame.Rect): Represents the AnimatedSprite's
            position on screen. Not an absolute position;
            relative position.
        active_frame_index (int): Frame # which is being
            rendered/to be rendered.
        animation_position (int): Animation position in
            milliseconds; milleseconds elapsed in this
            animation. This is used for determining
            which frame to select.

    See Also:

        * :class:`pygame.sprite.Sprite`
        * :class:`AnimatedSpriteFrame`

    """

    def __init__(self, frames):
        super(AnimatedSprite, self).__init__()
        self.frames = frames
        self.total_duration = self.total_duration(self.frames)
        self.active_frame_index = 0

        # animation position in milliseconds
        self.animation_position = 0

        # this gets updated depending on the frame/time
        # needs to be a surface.
        self.image = self.frames[0].surface

        # represents the animated sprite's position
        # on screen.
        self.rect = self.image.get_rect()

    def __getitem__(self, frame_index):

        return self.frames[frame_index]

    def largest_frame_size(self):
        """Goes by area.

        Returns:
            tuple (x, y): pixel dimensions of the largest
                frame surface in this AnimatedSprite.

        """

        largest_frame_size = (0, 0)

        for frame in self.frames:
            largest_x, largest_y = largest_frame_size
            largest_area = largest_x * largest_y

            frame_size = frame.surface.get_size()
            frame_x, frame_y = frame_size
            frame_area = frame_x * frame_y

            if frame_area > largest_area:
                largest_frame_size = (frame_size)

        return largest_frame_size

    @staticmethod
    def from_surface_duration_list(surface_duration_list):
        """Support PygAnimation-style frames.

        A list like [(surface, int duration in ms)]

        """

        running_time = 0
        frames = []

        for surface, duration in surface_duration_list:
            frame = AnimatedSpriteFrame(surface, running_time, duration)
            frames.append(frame)
            running_time += duration

        return AnimatedSprite(frames)

    @classmethod
    def from_file(cls, path_or_readable, anchors_config=None):
        """The default is to create from gif bytes, but this can
        also be done from other methods...

        """

        frames = cls.frames_from_gif(path_or_readable, anchors_config)

        return AnimatedSprite(frames)

    def active_frame(self):

        return self.frames[self.active_frame_index]

    def update(self, clock, absolute_position, viewport):
        self.animation_position += clock.get_time()

        if self.animation_position >= self.total_duration:
            self.animation_position = (self.animation_position %
                                       self.total_duration)
            self.active_frame_index = 0

        while (self.animation_position >
               self.frames[self.active_frame_index].end_time):

            self.active_frame_index += 1

        # NOTE: the fact that I'm using -1 here seems kinda sloppy,
        # because this is a hacky fix due to my own ignorance.
        self.image = self.frames[self.active_frame_index - 1].surface

        image_size = self.image.get_size()

        # NOTE: temporarily disabling this until i fully implement
        # absolute_position... in our current setup we never
        # touch the rect of frame surfaces, only the walkabout
        # relative_position = absolute_position.relative(viewport)
        relative_position = (0, 0)

        self.rect = pygame.rect.Rect(relative_position, image_size)

    @staticmethod
    def total_duration(frames):
        """Return the total duration of the animation in milliseconds,
        milliseconds, from animation frame durations.

        Args:
            frames (List[AnimatedSpriteFrame]): --

        Returns:
            int: The sum of all the frame's "duration" attribute.

        """

        return sum([frame.duration for frame in frames])

    @classmethod
    def frames_from_gif(cls, path_or_readable, anchors_config=None):
        """Create a list of surfaces (frames) and a list of their
        respective frame durations from an animated GIF.

        Args:
            path_or_readable (str|file-like-object): Path to
                an animated-or-not GIF.
            anchors_config (configparser): The anchors ini file
                associated with this GIF.

        Returns
            (List[pygame.Surface], List[int]): --

        """

        pil_gif = Image.open(path_or_readable)

        frame_index = 0
        frames = []
        time_position = 0

        try:

            while True:
                duration = pil_gif.info['duration']
                frame_sprite = cls.pil_image_to_pygame_surface(pil_gif, "RGBA")

                if anchors_config:
                    frame_anchors = LabeledSurfaceAnchors(
                                                          anchors_config,
                                                          frame_index
                                                         )
                else:
                    frame_anchors = None

                frame = AnimatedSpriteFrame(
                                            surface=frame_sprite,
                                            start_time=time_position,
                                            duration=duration,
                                            anchors=frame_anchors
                                           )
                frames.append(frame)
                frame_index += 1
                time_position += duration
                pil_gif.seek(pil_gif.tell() + 1)

        except EOFError:

            pass  # end of sequence

        return frames

    @staticmethod
    def pil_image_to_pygame_surface(pil_image, encoding):
        """Convert PIL Image() to pygame Surface.

        Args:
            pil_image (Image): image to convert to pygame.Surface().
            encoding (str): image encoding, e.g., RGBA

        Returns:
            pygame.Surface: the converted image

        Example:
            >>> import zipfile
            >>> from io import BytesIO
            >>> from PIL import Image
            >>> path = 'resources/walkabouts/debug.zip'
            >>> file_name = 'walk_north.gif'
            >>> sample = zipfile.ZipFile(path).open(file_name).read()
            >>> gif = Image.open(BytesIO(sample))
            >>> AnimatedSprite.pil_image_to_pygame_surface(gif, "RGBA")
            <Surface(6x8x32 SW)>

        """

        image_as_string = pil_image.convert('RGBA').tostring()

        return pygame.image.fromstring(
                                       image_as_string,
                                       pil_image.size,
                                       'RGBA'
                                      )

    def convert_alpha(self):
        """A runtime method for optimizing all of the
        frame surfaces of this animation.

        """

        for frame in self.frames:
            frame.surface.convert()
            frame.surface.convert_alpha()
