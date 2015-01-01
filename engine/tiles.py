# engine/tiles.py
# Lillian Lynn Mahoney <lillian.lynn.mahoney@gmail.com>
#
# This module is part of Untitled Game Engine and is released under the
# Attribution Assurance License: http://opensource.org/licenses/AAL

"""tile engine for maps.

See: http://en.wikipedia.org/wiki/Tile_engine

I just rewrote almost everything, so you'll have to wait for more
documentation...

Examples here!

"""

import os
import glob
import string
import cStringIO
import ConfigParser
import sqlite3
import pygame

__author__ = "Lillian Lynn Mahoney"
__copyright__ = "Copyright 2014, Lillian Lynn Mahoney"
__credits__ = ["Lillian Mahoney"]
__license__ = "Attribution Assurance License"
__maintainer__ = "Lillian Mahoney"
__email__ = "lillian.lynn.mahoney@gmail.com"
__status__ = "Development"


class BadTileName(Exception):
    """TileSwatch: non-existant tile name referenced"""

    def __init__(self, swatch_name, bad_tile_name):
        """Inform user of which tile name was attempted in vain.

        Args:
          swatch_name (str): the name of the swatch used, whereas a
            lookup for bad_tile_name was performed, but raised KeyError
          bad_tile_name (str): the tile name which was looked up, but
            didn't exist/have a corresponding value in swatch.

        """

        message = ('TileSwatch: no tile by name "%s"'  % (key, swatch_name))
        super(BatTileName, self).__init__(message)


class TileMap(object):
    """Represents a file object?"""

    def __init__(self, swatch_name, tile_graphic_names):
        # create the layer images and tile properties
        swatch = TileSwatch(swatch_name)
        first_layer = tile_graphic_names[0]
        dimensions_in_tiles = (
                               len(first_layer[0]),
                               len(first_layer),
                               len(tile_graphic_names)
                              )

        layer_width = len(first_layer[0]) * swatch.tile_size_x
        layer_height = len(first_layer) * swatch.tile_size_y
        layer_size = (layer_width, layer_height)

        tile_properties = [swatch.properties[x]
                           for y in first_layer for x in y]
        layer_images = []

        for z, layer in enumerate(tile_graphic_names):
            new_layer = pygame.Surface(layer_size)

            for y, row in enumerate(layer):

                for x, tile in enumerate(row):
                    tile_position = (x * swatch.tile_size_x,
                                     y * swatch.tile_size_y)
                    new_layer.blit(swatch[tile], tile_position)

            layer_images.append(new_layer)

        # impassability
        impassability = []
        layer_width_px, layer_height_px = layer_images[0].get_size()
        layer_width_tiles, layer_height_tiles, __ = dimensions_in_tiles

        for i, properties in enumerate(tile_properties):
            tile_x = i % layer_width_tiles
            tile_y = i / layer_width_tiles
            y = swatch.tile_size_y * tile_y
            x = swatch.tile_size_x * tile_x
            top_left_tile_corner = (x, y)

            if 'impass_all' in properties:
                rect = pygame.Rect(top_left_tile_corner, swatch.tile_size)
                properties.rect = rect
                impassability.append(rect)

        # attribs
        self.swatch = swatch
        self.tile_graphic_names = tile_graphic_names
        self.dimensions_in_tiles = dimensions_in_tiles
        self.layer_images = layer_images
        self.properties = tile_properties
        self.impassability = impassability

    def __getitem__(self, coord):
        """Fetch TileProperties by tile coordinate.

        Args:
          coord (tuple): (x, y) coordinate; z always just
            z-index (it's not a pixel value)

        Returns:
          TileProperties

        """

        x, y = coord
        width_in_tiles = self.layer_images.width_in_tiles

        return self.properties[(width_in_tiles * y) + x]

    def get_properties(self, coord):
        """Fetch TileProperties by pixel coordinate.

        Args:
          coord (tuple): (x, y) coordinate; z always just
            z-index (it's not a pixel value)

        Returns:
          TileProperties

        """

        tile_width, tile_height = self.layer_images.tile_size
        pixel_x, pixel_y = coord
        tile_x = pixel_x / tile_width
        tile_y = pixel_y / tile_height

        return self[(tile_x, tile_y)]

    def convert_layer_images(self):
        layer_images = self.layer_images

        for image in layer_images:
            image.convert()

        return None

    def to_string(self):
        """

        1. Define dimensions: map height, width, and layers
        2. tile names
        3. Finally, use a compression algo on the resulting string.

        """

        (width_in_tiles, height_in_tiles,
         total_layers) = self.dimensions_in_tiles
        dimensions_string = "%sx%sx%s" % self.dimensions_in_tiles
        swatch_string = self.swatch.name
        names = []

        for layer in self.tile_graphic_names:

            for row in layer:
                names.extend(row)

        tile_graphic_names = []

        for layer in self.tile_graphic_names:

            for row in layer:
                tile_graphic_names.extend(row)

        tile_graphic_names_string = ':'.join(tile_graphic_names)
        file_string = '\n'.join([
                                 dimensions_string,
                                 swatch_string,
                                 tile_graphic_names_string
                                ])

        return file_string


class TileSwatch(object):
    def __init__(self, swatch_name):
        """Named pygame.Surface instances of tiles in swatch directory.

        Abstraction of a directory of images
        accompanied by a config file.

        INI defines default tile properties, default tile.

        Args:
          swatch_name (str): asdf

        """

        swatch_directory = os.path.join('data', 'tiles', 'swatches',
                                        swatch_name)
        tile_pattern = os.path.join(swatch_directory, '*.png')
        self.swatch = {}
        self.properties = {}
        self.name = swatch_name

        # load default properties for tileswatch
        config_path = os.path.join(swatch_directory, 'swatch.ini')
        config = ConfigParser.RawConfigParser()
        config.read(config_path)

        for tile_name, properties in config.items('tile_properties'):
            props = TileProperties([p.strip() for p in properties.split(',')])
            self.properties[tile_name] = props

        # set swatch images
        for full_file_name in glob.iglob(tile_pattern):
            file_name, file_ext = os.path.splitext(full_file_name)
            file_name = os.path.split(file_name)[1]
            tile_image = pygame.image.load(full_file_name)
            self.tile_size = tile_image.get_size()
            self.tile_size_x, self.tile_size_y = self.tile_size
            self.swatch[file_name] = tile_image

    def __getitem__(self, tile_name):
        """Return tile corresponding to tile_name.

        Args:
          tile_name (str): tile/file name of desired tile

        Returns:
          pygame.Surface: tile image

        Raises:
          BadTileName: KeyError; no tile in swatch corresponds to
            provided tile_name.

        """

        try:

            return self.swatch[tile_name]

        except KeyError:

            raise BadTileName(self.name, tile_name)


class TileProperties(object):

    def __init__(self, properties=None, rect=None):
        """Tile info/properties/attributes.

        Currently Supported properties: impass_all.

        Args:
          properties (list): a list of strings, namely properties as
            seen above.
          rect (pygame.Rect): define if will be used for collision
            detection.

        Examples:
          >>> tile_properties = TileProperties(['teleport', 'sticky'])
          >>> "teleport" in tile_properties
          True
          >>> [p for p in tile_properties]
          ['teleport', 'sticky']

        """

        self.rect = rect

        if properties:
            self.properties = frozenset(properties)
        else:
            self.properties = frozenset()

    def __iter__(self):

        return iter(self.properties)

    def __contains__(self, item):

        return item in self.properties


def tilemap_from_string(tilemap_string):
    dimensions, swatch_name, tile_graphic_names = tilemap_string.split('\n')
    dimensions_in_tiles = dimensions.split('x')

    width, height, layers = dimensions_in_tiles
    width = int(width)
    height = int(height)
    layers = int(layers)

    tile_graphic_names_one_dimension = tile_graphic_names.split(':')
    tile_graphic_names_three_dimensions = []

    for layer_i in xrange(layers):
        layer = []

        for row_i in xrange(height):
            row = []

            for width_i in xrange(width):
                index = width_i + row_i * width + layer_i * width * height
                tile_graphic_name = tile_graphic_names_one_dimension[index]
                row.append(tile_graphic_name)

            layer.append(row)

        tile_graphic_names_three_dimensions.append(layer)

    return TileMap(swatch_name, tile_graphic_names_three_dimensions)


