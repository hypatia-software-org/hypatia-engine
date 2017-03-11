import os
import pygame

from hypatia.utils import pillow_image_to_pygame_surface
from PIL import Image 


class Frame:
    def __init__(self, surface, start_time, duration):
        """Create a frame.

        Args:
            surface (pygame.Surface): The surface for this frame.
            start_time (int): Millisecond that this frame starts.
            duration (int): Number of milliseconds this frame is displayed.
        """
        
        self.surface = surface
        self.start_time = start_time
        self.duration = duration 
        self.end_time = self.start_time + self.duration 


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames):
        super().__init__()

        self.frames = frames 
        self.total_duration = self.get_total_duration(frames)

        self.active_frame_idx = 0
        self.animation_position = 0

        self.image = frames[0].surface
        self.rect = self.image.get_rect()

    def update(self, timedelta):
        self.animation_position += timedelta

        if self.animation_position >= self.total_duration:
            self.animation_position = self.animation_position % self.total_duration

        # get the actual current frame
        while self.animation_position >= self.frames[self.active_frame_idx].end_time:
            self.active_frame_idx += 1

        # update our image to the current frame
        self.image = self.frames[self.active_frame_idx].surface
        self.rect = self.image.get_rect()

    @staticmethod
    def get_total_duration(frames):
        return sum([frame.duration for frame in frames])

    @classmethod
    def from_gif(cls, fileobj):
        """Returns an AnimatedSprite from the given GIF file object.
        """

        gif = Image.open(fileobj)

        frames = []
        time_pos = 0

        try:
            while True:
                duration = gif.info['duration']

                # get the image as a pygame surface
                frame_surface = pillow_image_to_pygame_surface(gif)

                # create a Frame with the given surface
                frame = Frame(frame_surface, time_pos, duration)
                frames.append(frame)

                # update our current position in time
                time_pos += duration

                # seek to next frame
                gif.seek(gif.tell() + 1)

        except EOFError:
            pass

        return cls(frames)