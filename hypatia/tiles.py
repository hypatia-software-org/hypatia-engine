# This module is part of Hypatia and is released under the
# MIT License: http://opensource.org/licenses/MIT

"""Where stuff is being drawn; tile engine for maps.

Load, save, and manipulate a tile map. A tile map is basically a sprite
which consists of graphical tiles aligned to a grid. Provides tools for
loading specific tile resources into an object. Contains information
about tiles (tile properties).

See Also:
    http://en.wikipedia.org/wiki/Tile_engine

"""

import os
import sys
import glob
import zlib
import string
import itertools
import xml.etree.ElementTree as ET

import pygame
import pyganim

from hypatia import util
from hypatia import animations


class BadTileID(Exception):
    """Tilesheet: tile was referenced by an
    ID which does not exist.

    Args:
        bad_tile_id (int): the tile id referenced which
            does not actually exist in a Tilesheet.

    Attributes:
        bad_tile_id (int): the tile ID referenced
            which does not exist.

    """

    def __init__(self, bad_tile_id):
        message = ('no tile by id #%d' % bad_tile_id)
        super(BadTileID, self).__init__(message)
        self.bad_tile_id = bad_tile_id


class TooManyTilesheets(Exception):
    """A TMX file was attempted to be imported through
    `TileMap.from_tmx()`, but the TMX defined more than
    one tilesheet. This is a feature Hypatia does not
    support.

    See Also:
        `TileMap.from_tmx()`:

    """

    def __init__(self):
        """The exception message is this class' docstring.

        Note:
            Mostly scaffolding, plus won't be here for long.

        """

        message = TooManyTilesheets.__docstring__
        super(TooManyTilesheets, self).__init__(message)
        self.bad_tile_id = bad_tile_id


class TMXVersionUnsupported(object):
    """Attempted to create a TileMap from a TMX map, but
    the TMX map version is unsupported.

    Attribs:
        map_version (str): the version which was attempted

    """

    def __init__(self, map_version):
        """

        Args:
            map_version (str): the map version which is
                unsupported. This becomes the map_version
                attribute.

        """

        message = 'version %s unsupported' % map_version
        super(TMXVersionUnsupported, self).__init__(message)
        self.map_version = map_version


class TMXLayersNotCSV(object):
    """The data encoding used for layers during Tilemap.from_tmx()
    is not supported. Only CSV is supported.

    Attribs:
        data_encoding (str): the failed data encoding.

    """

    def __init__(self, data_encoding):
        """

        Args:
            data_encoding (str): the failed data encoding

        """

        message = 'tmx layer data encoding %s unsupported' % data_encoding
        super(TMXLayersNotCSV, self).__init__(message)
        self.data_encodign = data_encoding


class TileMap(object):
    """Layers created from graphical tiles specified in a tilesheet.

    Note:
      Makes map-specific data accessible.

    Attributes:
      tilesheet:
      dimensions_in_tiles:
      layer_images:
      flags:
      impassability:
      animated_tiles:

    """

    def __init__(self, tilesheet_name, tile_ids):
        """Stitch tiles from swatch to layer surfaces.

        Piece together layers/surfaces from corresponding tile graphic
        names, using the specified tile swatch. Keep track of
        metadata, including passability.

        Args:
          tilesheet_name (str): directory name of the swatch to use
          tile_ids (list): 3d list where list[layer][row][tile]

        Examples:
          Make a 2x2x1 tilemap:
          >>> tiles = [[[0, 0], [0, 0]]]
          >>> tilemap = TileMap('debug', tiles)

        """

        # create the layer images and tile properties
        tilesheet = Tilesheet.from_resources(tilesheet_name)
        first_layer = tile_ids[0]

        width_tiles = len(first_layer[0])
        height_tiles = len(first_layer)
        depth_tiles = len(tile_ids)
        dimensions_in_tiles = (width_tiles, height_tiles, depth_tiles)

        tile_size = tilesheet.tiles[0].size
        tile_width, tile_height = tile_size
        layer_width = len(first_layer[0]) * tile_width
        layer_height = len(first_layer) * tile_height
        layer_size = (layer_width, layer_height)

        tiles = []
        layer_images = []
        impassable_rects = []
        animated_tile_stack = {i: set() for i in range(depth_tiles)}

        for z, layer in enumerate(tile_ids):
            new_layer = pygame.Surface(layer_size, pygame.SRCALPHA, 32)
            new_layer.fill([0, 0, 0, 0])

            for y, row_of_tile_ids in enumerate(layer):

                for x, tile_id in enumerate(row_of_tile_ids):
                    # is this right...?
                    tile_index = (((z - 1) * height_tiles * width_tiles) +
                                  (y * width_tiles) + x)
                    tile = tilesheet[tile_id]

                    # if not on first layer, merge flags down to first
                    if z:
                        tile_index = (y * width_tiles) + x
                        tiles[tile_index].flags.update(tile.flags)
                    else:
                        tiles.append(tile)

                    # -1 is air/nothing
                    if tile.tilesheet_id == -1:

                        continue

                    # blit tile subsurface onto respective layer
                    tile_position = (x * tile_width, y * tile_height)
                    new_layer.blit(tile.subsurface, tile_position)

                    # is this tile an animation?
                    if tile.tilesheet_id in tilesheet.animated_tiles:
                        animated_tile = (tilesheet.
                                         animated_tiles[tile.tilesheet_id])
                        animation_info = (animated_tile, tile_position)
                        animated_tile_stack[z].add(animation_info)

                    # finally passability!
                    if 'impass_all' in tile.flags:
                        impassable_rects.append(pygame.Rect(tile_position,
                                                            tile_size))

            layer_images.append(new_layer)

        self.tilesheet = tilesheet
        self.layer_images = layer_images
        self.tiles = tiles
        self.impassable_rects = impassable_rects
        self.animated_tile_stack = animated_tile_stack
        self.dimensions_in_tiles = dimensions_in_tiles
        self._tile_ids = tile_ids

    def __getitem__(self, coord):
        """Fetch TileInfo by tile coordinate.

        Args:
          coord (tuple): (x, y) coordinate; z always just
            z-index (it's not a pixel value)

        Returns:
          TileProperties

        Examples:
          >>> tiles = [[[0, 0], [0, 0]]]
          >>> tilemap = TileMap('debug', tiles)
          >>> 'impass_all' in tilemap[(1, 1)].flags
          True

        """

        x, y = coord
        width_in_tiles = self.dimensions_in_tiles[0]

        return self.tiles[coord_to_index(width_in_tiles, x, y)]

    def get_info(self, coord):
        """Fetch TileProperties by pixel coordinate.

        Args:
          coord (tuple): (int x, int y) coordinate;  units in pixels.
            Coord only has to be in the area of tile.

        Returns:
          TileInfo

        Examples:
          Let's assume 10x10 tiles...
          >>> tiles = [[[0, 10], [-1, 4]]]
          >>> tilemap = TileMap('debug', tiles)
          >>> 'impass_all' in tilemap.get_info((12, 12)).flags
          True

        """

        tile_width, tile_height = self.tilesheet.tile_size
        pixel_x, pixel_y = coord
        tile_x = pixel_x // tile_width
        tile_y = pixel_y // tile_height

        return self[(tile_x, tile_y)]

    def blit_layer_animated_tiles(self, viewport, layer):

        for tile_pyganim, position in self.animated_tile_stack[layer]:
            tile_pyganim.blit(viewport.surface,
                              viewport.relative_position(position))

    def runtime_setup(self):
        """This is for game.py. These need to be launched after pygame
        has started.

        """

        layer_images = self.layer_images

        for image in layer_images:
            image.convert()
            image.convert_alpha()

        for i, tile_pyganim in self.tilesheet.animated_tiles.items():
            tile_pyganim.convert()
            tile_pyganim.convert_alpha()
            tile_pyganim.play()

        return None

    def to_tmx(self):
        "Scaffolding"""
        pass

    def to_string(self, separator=' '):
        """Create the user-unfriendly string for the tilemap.

        Args:
          separator (str): can be ''

        """

        output_string = ''

        # create map layers
        layers = []
        max_digits = len(str(len(self.tilesheet.tiles))) - 1
        id_format = '%0' + str(max_digits) + 'd'

        for layer in self._tile_ids:
            layer_lines = []

            for row in layer:
                row_string = separator.join([id_format % i for i in row])

                layer_lines.append(row_string)

            layer_string = '\n'.join(layer_lines)
            layers.append(layer_string)

        layers_string = '\n\n'.join(layers)
        output_string += layers_string

        return self.tilesheet.name + '\n' + output_string

    @classmethod
    def from_tmx(cls, tmx_file_like_object):
        """Create a TileMap from Tiled's "Tile Map XML" map
        format. For more information please see the official
        TMX documentation:

          * http://doc.mapeditor.org/reference/tmx-map-format/

        The TMX must use CSV for layers. You also have to make
        sure that the filename used in tile source is exactly
        the same as the TileSheet you wanna use.

        HOW DO YOU DEFINE NPCS AND PLAYER START???

        Args:
            tmx_file_like_object: --

        Returns:
            TileMap

        Note:
            Yes, I created this because I thought pytmx and
            tmxlib didn't suit my purposes.

        """

        tree = ET.parse(tmx_file_like_object)
        root = tree.getroot()

        # check the version first, make sure it's supported
        map_version = root.find('./map').attrib['version']

        if map_version != "1.0":

            raise TMXVersionUnsupported(ap_version)

        # Get the Tilesheet (tileset) name from the tileset
        # image source.
        tileset_images = root.findall('./map/tileset/image')

        if len(tileset_images) > 1:

            raise TooManyTilesheets()

        file_path = tileset_images[0].attrib['source']
        file_name = os.path.basename(file_path)
        tilesheet_name = os.path.splitext(file_name)[0]

        # get the 3D constructor/blueprint of TileMap,
        # which simply references, by integer, the
        # tile from tilesheet.
        layers = []

        for layer_data in root.findall("./map/layer/data"):
            data_encoding = layer_data.attrib['encoding']

            if data_encoding != 'csv':

                raise TMXLayersNotCSV(data_encoding)
                
            layer_csv = layer_data.text
            rows = layer_csv.split('\n')
            parsed_rows = []

            for row in rows:
                parsed_row = [int(tile_id) for tile_id in row.split(',')]
                parsed_rows.append(parsed_row)

            layers.append(parsed_rows)

        return TileMap(tilesheet_name, layers)

    @classmethod
    def from_string(cls, map_string, separator=' '):
        """This is a debug feature. Create a 3D list of tile names using
        ASCII symbols. Supports layers.

        """

        # GET TILESHEET NAME FROM THE FIRST LINE, REMOVE FIRST LINE
        tilesheet_name, layers_string = map_string.split('\n', 1)

        # NOTE: I'm using strip('\n') because I can't seem to make
        # the \n at the end of map-string.txt to go away.
        # watch the quirky wording; layers_string >> layer_strings
        layer_strings = layers_string.strip('\n').split('\n\n')

        # transform our characters into a 3D list of tile graphic names
        layers = []

        for layer_string in layer_strings:
            layer = [[int(tile_id) for tile_id in row.split(separator)]
                     for row in layer_string.split('\n')]
            layers.append(layer)

        return TileMap(tilesheet_name, layers)


class Tilesheet(object):
    """An image consisting of uniformly sized squares called "tiles."

    Attributes:
      name (str): --
      surface (pygame.Surface): --
      tiles (iter): --
      tile_size (tuple): (x, y) pixel dimensions of the tiles which
        comprise the Tilesheet surface.
      animated_tiles (dict): tile_id -> pyganimation

    """

    def __init__(self, name, surface, tiles, tile_size, animated_tiles=None):
        """

        Args:
          name (str): --
          surface (pygame.Surface): --
          tiles (iter): --
          tile_size (tuple): (x, y) pixel dimensions of the tiles which
            comprise the Tilesheet surface.
          animated_tiles (dict): tile_id -> pyganimation

        """

        self.name = name
        self.surface = surface
        self.tiles = tiles
        self.tile_size = tile_size
        self.animated_tiles = animated_tiles

    def __getitem__(self, tile_id):

        try:

            return self.tiles[tile_id]

        except IndexError:

            raise BadTileID(tile_id)

    @classmethod
    def from_resources(cls, tilesheet_name):
        """Create a Tilesheet from a name, corresponding to a path
        pointing to a tilesheet zip archive.

        Args:
          tilesheet_name (str): this string is appended to the default
            resources/tilesheets location.

        Returns:
          Tilesheet: initialized utilizing information from the
            respective tilesheet zip's tilesheet.png and tilesheet.ini.

        """

        # path to the zip containing tilesheet.png and tilesheet.ini
        resource = util.Resource('tilesheets', tilesheet_name)
        zip_path = os.path.join(
                                'resources',
                                'tilesheets',
                                tilesheet_name + '.zip'
                               )
        tilesheet_surface = pygame.image.load(resource['tilesheet.png'])
        config = resource['tilesheet.ini']

        # build the meta
        flags = {int(k): set(v.split(',')) for k, v in config.items('flags')}
        tile_width = config.getint('meta', 'tile_width')
        tile_height = config.getint('meta', 'tile_height')
        tile_size = (tile_width, tile_height)
        tilesheet_width, tilesheet_height = tilesheet_surface.get_size()
        tilesheet_width_in_tiles = tilesheet_width // tile_width
        tilesheet_height_in_tiles = tilesheet_height // tile_height
        total_tiles = tilesheet_width_in_tiles * tilesheet_height_in_tiles

        # tile initialization; buid all the tiles
        tiles = []

        for tilesheet_id in range(total_tiles):
            tile = Tile(tilesheet_id=tilesheet_id,
                        tilesheet_surface=tilesheet_surface,
                        tile_size=tile_size,
                        flags=flags.get(tilesheet_id, None))
            tiles.append(tile)

        # for effects and animations
        animated_tiles = {}

        # if animations are present, let's piece together some
        # PygAnimations using tile data.
        if config.has_section('animations'):
            # used for checking which animation we're on
            seen_tile_ids = set()
            frame_buffer = []

            for tile_id, animation_string in config.items('animations'):
                tile_id = int(tile_id)
                frame_duration, next_tile_id = animation_string.split(',')
                frame_duration = float(frame_duration)
                next_tile_id = int(next_tile_id)
                frame_buffer.append((tiles[tile_id].subsurface,
                                     frame_duration))

                if next_tile_id in seen_tile_ids:
                    tile_pyganim = pyganim.PygAnimation(frame_buffer)
                    animated_tiles[next_tile_id] = tile_pyganim
                    frame_buffer = []
                    seen_tile_ids = set()

                seen_tile_ids.add(tile_id)

        # functions which return a PygAnimation, and accept a surface
        if config.has_section('animate_effect'):
            effects = {'cycle': animations.palette_cycle}

            for tile_id, effect in config.items('animate_effect'):
                tile_id = int(tile_id)
                corresponding_tile = tiles[tile_id].subsurface
                animated_tiles[tile_id] = effects[effect](corresponding_tile)

        return Tilesheet(tilesheet_name, tilesheet_surface,
                         tiles, tile_size, animated_tiles)


class Tile(object):
    """A graphical map tile, referencing a rectangular area on a
    tilesheet (reference surface), with meta data.

    Attributes:

    """

    def __init__(self, tilesheet_id, tilesheet_surface, tile_size, flags=None):
        """create subsurface of tilesheet surface using topleft
        position on tilesheet.

        Args:
          tilesheet_id (int): Index belonging to this Tile in its
            respective Tilesheet. The tile number on a Tilesheet.
          tilesheet_surface (Surface): Surface used for
            creating Tile subsurface.
          tile_size (tuple): (x, y) where x and y are integers
            defining the pixel dimensions of a tile.
          flags (set): Set of strings which acts as attributes, e.g.,
            "impass_all."

        """

        tilesheet_width_in_tiles = (tilesheet_surface.get_size()[0] /
                                    tile_size[0])
        top_left_in_tiles = index_to_coord(tilesheet_width_in_tiles,
                                           tilesheet_id)
        subsurface_top_left = (top_left_in_tiles[0] * tile_size[0],
                               top_left_in_tiles[1] * tile_size[1])
        position_rect = pygame.Rect(subsurface_top_left, tile_size)
        self.area_on_tilesheet = position_rect
        self.subsurface = tilesheet_surface.subsurface(position_rect)
        self.flags = flags or set()
        self.tilesheet_id = tilesheet_id
        self.size = tile_size


def coord_to_index(width, x, y):
    """Return the 1D index which corresponds to 2D position (x, y).

    Examples:
      If we have a 2D grid like this:

      0 1 2
      3 4 5
      6 7 8

      We can assert that element 8 is of the coordinate (2, 2):
      >>> 8 == coord_to_index(3, 2, 2)
      True

    """

    return (width * y) + x


def index_to_coord(width, i):
    """Return the 2D position (x, y) which corresponds to 1D index.

    Examples:
      If we have a 2D grid like this:

      0 1 2
      3 4 5
      6 7 8

      We can assert that element 8 is of the coordinate (2, 2):
      >>> (2, 2) == index_to_coord(3, 8)
      True

    """

    if i == 0:

        return (0, 0)

    else:

        return ((i % width), (i // width))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
