# py.test/test_tiles.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia and is released under the
# MIT license: http://opensource.org/licenses/MIT

"""py.test unit testing for engine/tiles.py

Run py.test on this module to assert hypatia.tiles is completely functional.

"""

from hypatia import tiles
import pygame

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2015, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


def test_coord_to_index():
    # coords_to_index(row_width, x, y)

    #    0  1  2
    #------------
    # 0| 00 01 02
    # 1| 03 04 05
    # 2| 06 07 08
    assert tiles.coord_to_index(3, 2, 2) == 8

    #    0  1  2  3  4
    #------------------
    # 0| 00 01 02 03 04
    # 1| 05 06 07 08 09
    # 2| 10 11 12 13 14
    assert tiles.coord_to_index(5, 4, 2) == 14


# NOTE: unfinished!
def test_tile():
    # first let's be clear about our variables
    faux_tilesheet = pygame.Surface((800, 600))
    tile_id = 1
    tile_size = (10, 10)
    tile_flags = set(['impass_all'])
    subsurface_topleft = (20, 30)

    # now let's test Tile()...
    tile = tiles.Tile(tile_id, faux_tilesheet, tile_size, subsurface_topleft, tile_flags)
    assert tile.size == tile_size
    assert tile.id == tile_id

