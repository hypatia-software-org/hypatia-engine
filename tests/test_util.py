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
import pyganim

from hypatia import util

try:
    os.chdir('demo')
except OSError:
    pass


def test_resource():
    """Test the util.Resource class.

    """

    resource = util.Resource('walkabouts', 'debug')

    assert 'walk_north.gif' in resource
    assert isinstance(resource['walk_north.gif'], pyganim.PygAnimation)
    assert isinstance(resource['walk_north.ini'], configparser.ConfigParser)
