# engine/tiles.py
# Lillian Lemmer <lillian.lynn.lemmer@gmail.com>
#
# This module is part of Hypatia Engine and is released under the
# MIT License: http://opensource.org/licenses/MIT

"""Where stuff is being drawn; tile engine for maps.

Load, save, and manipulate a tile map. A tile map is basically a sprite
which consists of graphical tiles aligned to a grid. Provides tools for
loading specific tile resources into an object. Contains information
about tiles (tile properties).

For more information see: http://en.wikipedia.org/wiki/Tile_engine

Important equation: (width_in_tiles * y) + x

"""

import os
import sys
import glob
import zlib
import string

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

import pygame

__author__ = "Lillian Lemmer"
__copyright__ = "Copyright 2015, Lillian Lemmer"
__credits__ = ["Lillian Lemmer"]
__license__ = "MIT"
__maintainer__ = "Lillian Lemmer"
__email__ = "lillian.lynn.lemmer@gmail.com"
__status__ = "Development"


class BadTileName(Exception):
    """TileSwatch: non-existant tile name referenced. Inform the user
    of which tile name was attempted in vain

    Args:
      swatch_name (str): the name of the swatch used, whereas a
        lookup for bad_tile_name was performed, but raised KeyError
      bad_tile_name (str): the tile name which was looked up, but
        didn't exist/have a corresponding value in swatch.

    Attributes:
      message: printed error message; prints the tile name attempted

    """

    def __init__(self, swatch_name, bad_tile_name):
        message = ('TileSwatch: no tile by name "%s"'  % bad_tile_name)
        super(BadTileName, self).__init__(message)


class TileMap(object):
    """Layers created from graphical tiles specified in a tile swatch.

    Note:
      Makes map-specific data accesssible.

    Attributes:
      swatch:
      tile_graphic_names:
      dimensions_in_tiles:
      layer_images:
      properties:
      impassability:
      animated_tiles:
      npcs:

    """

    def __init__(self, swatch_name, tile_graphic_names, npcs=None):
        """Stitch tiles from swatch to layer surfaces. 

        Piece together layers/surfaces from corresponding tile graphic
        names, using the specified tile swatch. Keep track of
        metadata, including passability.

        Args:
          swatch_name (str): directory name of the swatch to use
          tile_graphic_names (list): 3d list where
            list[layer][row][tile]
          npcs (list): list of player.Npc objects

        Examples:
          Make a 2x2x1 tilemap:
          >>> tiles = [['default', 'default'], ['default', 'default']]
          >>> tilemap = TileMap('debug', tiles)

        """

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

        # bug: does not use master default properties
        # unions properties from higher z-index down
        tile_properties = []

        for z, layer in enumerate(tile_graphic_names):
        
            for y, row_of_image_names in enumerate(layer):

                for x, image_name in enumerate(row_of_image_names):
                
                    if image_name in swatch.properties:
                        properties = swatch.properties[image_name]
                    else:
                        properties = TileProperties()
                
                    if z:
                        # check tile_properties[(width_in_tiles * y) + x]
                        # union THIS with existing
                        (tile_properties[(dimensions_in_tiles[0] * y) + x] +
                         properties)
                    else:
                        tile_properties.append(properties)

        # make the layer images
        layer_images = []

        for z, layer in enumerate(tile_graphic_names):
            new_layer = pygame.Surface(layer_size, pygame.SRCALPHA, 32)
            new_layer.fill([0,0,0,0])

            for y, row in enumerate(layer):

                for x, tile in enumerate(row):

                    if tile == 'air':

                        continue

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
            tile_y = i // layer_width_tiles
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
        self.npcs = npcs
        
        self.convert_layer_images()

    def __getitem__(self, coord):
        """Fetch TileProperties by tile coordinate.

        Args:
          coord (tuple): (x, y) coordinate; z always just
            z-index (it's not a pixel value)

        Returns:
          TileProperties

        Examples:
          >>> tiles = [['default', 'default'], ['default', 'water']]
          >>> tilemap = TileMap('debug', tiles)
          >>> 'impass_all' in tilemap[(1, 1)].properties
          True

        """

        x, y = coord
        width_in_tiles = self.dimensions_in_tiles[0]

        return self.properties[(width_in_tiles * y) + x]

    def get_properties(self, coord):
        """Fetch TileProperties by pixel coordinate.

        Args:
          coord (tuple): (int x, int y) coordinate;  units in pixels.
            Coord only has to be in the area of tile.

        Returns:
          TileProperties

        Examples:
          Let's assume 10x10 tiles...
          >>> tiles = [['default', 'default'], ['default', 'water']]
          >>> tilemap = TileMap('debug', tiles)
          >>> 'impass_all' in tilemap.get_properties((12, 12)).properties
          True

        """

        tile_width, tile_height = self.layer_images[0].get_size()
        pixel_x, pixel_y = coord
        tile_x = pixel_x // tile_width
        tile_y = pixel_y // tile_height

        return self[(tile_x, tile_y)]

    def convert_layer_images(self):
        """Call once pygame screen is init'd for efficiency.

        """

        layer_images = self.layer_images

        for image in layer_images:
            image.convert()
            image.convert_alpha()

        return None

    def to_string(self):
        """Create a string which can be used to
        recreate that same tilemap.

        Note:
          The format for the string is such:
            Line 1: tilemap height, width, and layers
            Line 2: swatch name
            Line 3: tile names

          The resulting string is then compressed.

        Returns:
          str: string which can recreate the TileMap

        Examples:
           >>> tilemap_string = tilemap.to_string()
           >>> fh = open('somefile.tilemap', 'w')
           >>> fh.write(tilemap_string)
           >>> fh.close()

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

        return zlib.compress(file_string.encode('ascii'), 9)


class TileSwatch(object):

    def __init__(self, swatch_name):
        """Named pygame.Surface instances of tiles in swatch directory.

        Note:
          Abstraction of a directory of images
          accompanied by a config file.

          INI defines default tile properties, default tile.

          need to load sprite.Animation for animated gifs loaded as tiles.j animated tiles hae support for effects like shift_pallette

        Args:
          swatch_name (str): asdf

        Examples:
          >>> tileswatch = TileSwatch('debug')

        """

        swatch_directory = os.path.join(
                                        '../resources',
                                        'tileswatches',
                                        swatch_name
                                       )
        swatch_directory = os.path.abspath(swatch_directory)
        tile_pattern = os.path.abspath(os.path.join(swatch_directory, '*.png'))
        self.swatch = {}
        self.properties = {}
        self.name = swatch_name

        # load default properties for tileswatch
        # make sure it's loaded first, I guess
        config_path = os.path.abspath(os.path.join(
                                                   swatch_directory,
                                                   'swatch.ini'
                                                  )
                                     )

        if not os.path.exists(config_path):

            raise Exception('bad config path: ' + config_path)

        config_file = configparser.RawConfigParser()
        config_file.read(config_path)

        for tile_name, properties in config_file.items('tile_properties'):
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

        Examples:
          >>> swatch['water']
          <pygame.Surface>

        """

        try:

            return self.swatch[tile_name]

        except KeyError:

            raise BadTileName(self.name, tile_name)


class TileProperties(object):
    """Tile info/properties/attributes.

    Note:
      Currently supported properties: impass_all.

    Attributes:
      rect:
      properties:

    """

    def __init__(self, properties=None, rect=None):
        """Create a frozenset which describes the properties of a tile.

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

        # rect should always be present for positioning info
        # impassable should be set if "impassable" in properties
        # then set self.impassable = true or self.solid = true
        self.rect = rect

        if properties:
            self.properties = set(properties)
        else:
            self.properties = set()

    def __iter__(self):

        return iter(self.properties)

    def __contains__(self, item):

        return item in self.properties
        
    def __add__(self, other_tileproperties):
        self.properties.update(other_tileproperties.properties)
        
        if other_tileproperties.rect:
            self.rect = other_tileproperties.rect

    def merge_properties(self, new_properties):
        self.properties.update(new_properties)


def tilemap_from_string(tilemap_string):
    """Create a TileMap instance from a string.

    Args:
      tilemap_string (str): string generated by TileMap.to_string().

    Retuns:
      TileMap: TileMap instance created from tilemap_string.

    """

    tilemap_decompressed = zlib.decompress(tilemap_string)
    tilemap_string = tilemap_decompressed.decode('ascii')
    dimensions, swatch_name, tile_graphic_names = tilemap_string.split('\n')
    dimensions_in_tiles = dimensions.split('x')

    width, height, layers = dimensions_in_tiles
    width = int(width)
    height = int(height)
    layers = int(layers)

    tile_graphic_names_one_dimension = tile_graphic_names.split(':')
    tile_graphic_names_three_dimensions = []

    for layer_i in range(layers):
        layer = []

        for row_i in range(height):
            row = []

            for width_i in range(width):
                index = width_i + row_i * width + layer_i * width * height
                tile_graphic_name = tile_graphic_names_one_dimension[index]
                row.append(tile_graphic_name)

            layer.append(row)

        tile_graphic_names_three_dimensions.append(layer)

    return TileMap(swatch_name, tile_graphic_names_three_dimensions)


def blueprint_from_string(blueprint_string):
    """This is a debug feature. Create a 3D list of tile names using
    ASCII symbols.

    Note:
      Supports layering!

      ` grass
      # cobblestone_wall
      ~ water
      A air
      v column_top
      ^ column_bottom
      
      `###```~`
      `###```~`
      `###```~`
      ```````~`

      AAAAAAAAv
      AAAAAAAA^
      AAAAAAAAv
      AAAAAAAA^
      
    """

    # firstly, split the string by blank line. this will give us the
    # legend and following layers
    blueprint_split = blueprint_string.split('\n\n')
    legend_string = blueprint_split[0]
    blueprint_strings = blueprint_split[1:]
    legend = {}

    for line in legend_string.split('\n'):

        symbol, tile_name = line.split(' ', 1)
        legend[symbol] = tile_name

    layers = []

    for layer_string in blueprint_strings:
        layer = []
        
        for line in layer_string.split('\n'):
            row = [legend[char] for char in line]
            layer.append(row)
            
        layers.append(layer)

    return layers

