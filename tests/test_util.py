# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""py.test unit testing for hypatia/util.py

Run py.test on this module to assert hypatia.util
is completely functional.

"""

import os

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

import pygame
import pytest

from hypatia import util
from hypatia import animatedsprite

try:
    os.chdir('demo')
except OSError:
    pass


def test_resource():
    """Test the util.Resource class.

    """

    resource = util.Resource('walkabouts', 'debug')

    # Assure that the "walk_north.gif" (which is default in the
    # debug resources) exists in resource, and that the magic
    # method for membership testing (__contains__) works.
    assert 'walk_north.gif' in resource

    # Assure GIF files are loading AnimatedSprite objects
    assert (isinstance(resource['walk_north.gif'],
            animatedsprite.AnimatedSprite))

    # Assure INI files are loading as ConfigParser objects
    assert isinstance(resource['walk_north.ini'], configparser.ConfigParser)
