# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""These are utilities which are commonly utilized
by all modules in Hypatia. It serves for the ugly,
underlying components of miscellaneous actions which
assist other modules, and does not do much on its own.

"""

import os
import zipfile
from io import BytesIO

try:
    import ConfigParser as configparser
    from cStringIO import StringIO

except ImportError:
    import configparser
    from io import StringIO

import pygame
import pyganim
from PIL import Image


class Resource(object):
    """A zip archive in the resources directory, located by
    supplying a resource category and name. Files are stored
    as a str, BytesIO, PygAnimation, or ConfigParser, in a
    dictionary. Files are referenced by filepath/filename.

    Attributes:
        files (dict): Key is file name, value can be one of str,
            BytesIO, PygAnim, or ConfigParser objects.

    Example:
        >>> import pyganim
        >>> resource = Resource('walkabouts', 'debug')
        >>> 'walk_north.gif' in resource
        True
        >>> isinstance(resource['walk_north.gif'], pyganim.PygAnimation)
        True
        >>> resource = Resource('scenes', 'debug')
        >>> resource['tilemap.txt'].startswith('debug')
        True

    """

    def __init__(self, resource_category, resource_name):
        """Load a resource ZIP using a category and zip name.

        Args:
            resource_category (str): E.g., tilesheets, walkabouts.
            resource_name (str): E.g., debug.

        """

        path = os.path.join(
                            'resources',
                            resource_category,
                            resource_name
                           )

        file_handlers = {
                         '.ini': configparser_fromfp,
                         '.gif': load_gif
                        }

        files = {}

        # choose between loading as an unpacked directory, or a zip file.
        # unpacked takes priority.

        if os.path.isdir(path):

            for file_name in os.listdir(path):
                file_data = open(os.path.join(path, file_name)).read()
                files[file_name] = file_data
        else:
            with zipfile.ZipFile(path + ".zip") as zip_file:

                for file_name in zip_file.namelist():
                    # because namelist will also generate
                    # the directories
                    if not file_name:

                        continue

                    file_data = zip_file.open(file_name).read()
                    files[file_name] = file_data

        # now do post-processing
        for file_name in files.keys():
            file_data = files[file_name]

            try:
                file_data = file_data.decode('utf-8')
            except ValueError:
                file_data = BytesIO(file_data)

            # then we do the file handler call ehre
            file_extension = os.path.splitext(file_name)[1]

            if file_extension in file_handlers:
                file_data = file_handlers[file_extension](file_data)

            files[file_name] = file_data

        self.files = files

    def __getitem__(self, file_name):

        return self.files[file_name]

    def __contains__(self, item):

        return item in self.files

    def get_type(self, file_extension):
        """Return a dictionary of files which have the file extension
        specified. Remember to include the dot, e.g., ".gif"!

        Arg:
            file_extension (str): the file extension (including dot) of
                the files to return.

        Warning:
            Remember to include the dot in the file extension, e.g., ".gif".

        Returns:
            dict|None: {file name: file content} of files which have the
                file extension specified. If no files match,
                None is returned.

        """

        matching_files = {}

        for file_name, file_content in self.files.items():

            if os.path.splitext(file_name)[1] == file_extension:
                matching_files[file_name] = file_content

        return matching_files or None


def load_gif(path_or_bytesio):
    """Create a PygAnim object by reading a GIF from path or
    a BytesIO object.

    Args:
        path_or_bytesio (str|BytesIO): create animation using either
            a string file path to a GIF, or provide a BytesIO of a GIF.

    Returns:
        PygAnim: the PygAnim animation which accurately depicts the GIF
            referenced in gif_path.

    Example:
        >>> path = 'resources/walkabouts/debug.zip'
        >>> file_name = 'walk_north.gif'
        >>> sample = zipfile.ZipFile(path).open(file_name).read()
        >>> load_gif(BytesIO(sample))
        <pyganim.PygAnimation object at 0x...>

    """

    pil_gif = Image.open(path_or_bytesio)

    frame_index = 0
    frames = []

    try:

        while 1:
            duration = pil_gif.info['duration'] / 1000.0
            frame_as_pygame_image = pil_to_pygame(pil_gif, "RGBA")
            frames.append((frame_as_pygame_image, duration))
            frame_index += 1
            pil_gif.seek(pil_gif.tell() + 1)

    except EOFError:

        pass  # end of sequence

    gif = pyganim.PygAnimation(frames)
    gif.anchor(pyganim.CENTER)

    return gif


def pil_to_pygame(pil_image, encoding):
    """Convert PIL Image() to pygame Surface.

    Args:
        pil_image (Image): image to convert to pygame.Surface().
        encoding (str): image encoding, e.g., RGBA

    Returns:
        pygame.Surface: the converted image

    Example:
        >>> from PIL import Image
        >>> path = 'resources/walkabouts/debug.zip'
        >>> file_name = 'walk_north.gif'
        >>> sample = zipfile.ZipFile(path).open(file_name).read()
        >>> gif = Image.open(BytesIO(sample))
        >>> pil_to_pygame(gif, "RGBA")
        <Surface(6x8x32 SW)>

    """

    image_as_string = pil_image.convert('RGBA').tostring()

    return pygame.image.fromstring(
                                   image_as_string,
                                   pil_image.size,
                                   'RGBA'
                                  )


def configparser_fromfp(file_data):
    file_data = StringIO(file_data)
    config = configparser.ConfigParser()

    # NOTE: this still works in python 3, though it was
    # replaced by config.read_file()
    config.readfp(file_data)

    return config
