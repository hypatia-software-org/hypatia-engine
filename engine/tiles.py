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

        layer_width = len(first_layer[0]) * swatch.tile_size[0]
        layer_height = len(first_layer) * swatch.tile_size[1]
        layer_size = (layer_width, layer_height)

        tileinfos = []

        for z, layer in enumerate(tile_graphic_names):
        
            for y, row_of_image_names in enumerate(layer):

                for x, image_name in enumerate(row_of_image_names):
                
                    if image_name in swatch.info:
                        tileinfo = swatch.info[image_name]
                    else:
                        tileinfo = TileInfo(image_name)
                
                    if z:
                        # check tile_properties[(width_in_tiles * y) + x]
                        # union THIS with existing
                        (tileinfos[(dimensions_in_tiles[0] * y) + x] +
                         tileinfo)
                    else:
                        tileinfos.append(tileinfo)

        # make the layer images
        layer_images = []

        for z, layer in enumerate(tile_graphic_names):
            new_layer = pygame.Surface(layer_size, pygame.SRCALPHA, 32)
            new_layer.fill([0,0,0,0])

            for y, row in enumerate(layer):

                for x, tile in enumerate(row):

                    if tile == 'air':

                        continue

                    tile_position = (x * swatch.tile_size[0],
                                     y * swatch.tile_size[1])
                    new_layer.blit(swatch[tile], tile_position)

            layer_images.append(new_layer)

        # impassability
        impassability = []
        layer_width_px, layer_height_px = layer_images[0].get_size()
        layer_width_tiles, layer_height_tiles, __ = dimensions_in_tiles

        for i, tileinfo in enumerate(tileinfos):
            tile_x = i % layer_width_tiles
            tile_y = i // layer_width_tiles
            y = swatch.tile_size[1] * tile_y
            x = swatch.tile_size[0] * tile_x
            top_left_tile_corner = (x, y)

            if 'impass_all' in tileinfo.flags:
                rect = pygame.Rect(top_left_tile_corner, swatch.tile_size)
                tileinfo.rect = rect
                impassability.append(rect)

        # attribs
        self.swatch = swatch
        self.tile_graphic_names = tile_graphic_names
        self.dimensions_in_tiles = dimensions_in_tiles
        self.layer_images = layer_images
        self.info = tileinfos
        self.impassability = impassability
        self.npcs = npcs
        
        self.convert_layer_images()

    def __getitem__(self, coord):
        """Fetch TileInfo by tile coordinate.

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

        return self.info[(width_in_tiles * y) + x]

    def get_info(self, coord):
        """Fetch TileProperties by pixel coordinate.

        Args:
          coord (tuple): (int x, int y) coordinate;  units in pixels.
            Coord only has to be in the area of tile.

        Returns:
          TileInfo

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

    def to_string(self, friendly=False):
        """Create the user-unfriendly string for the tilemap.
        
        """
        
        output_string = ''

        # create legend if friendly
        if friendly:
            tile_graphic_names = []
            
            for layer in self.tile_graphic_names:
            
                for row in layer:
                    tile_graphic_names.extend(row)
                    
            tile_graphic_names = set(tile_graphic_names)
            legend = {}  # name to char
            printable_chars = string.printable
            
            for i, tile_graphic_name in enumerate(tile_graphic_names):
                symbol = printable_chars[i]
                legend[tile_graphic_name] = symbol
                output_string += symbol + ' ' + tile_graphic_name + '\n'
            
            output_string += '\n'
                    
        # create map layers
        layers = []
        
        for layer in self.tile_graphic_names:
            layer_lines = []
        
            for row in layer:
                    
                if friendly:
                    row_string = ''.join([legend[name] for name in row])
                else:
                    row_string = ';'.join(row)
                    
                layer_lines.append(row_string)
                    
            layer_string = '\n'.join(layer_lines)
            layers.append(layer_string)

        layers_string = '\n\n'.join(layers)
        output_string += layers_string

        if friendly:
        
            return output_string
            
        else:
        
            return zlib.compress(output_string.encode('ascii'), 9)

    @classmethod
    def from_string(cls, blueprint_string, friendly=False):
        """This is a debug feature. Create a 3D list of tile names using
        ASCII symbols. Supports layers.
       
        Note:
          In the future, there will be more "positionals" which follow
          the legend block, e.g., npcs, which would then be followed by
          all of the layers.
          
          What about swatch name? Shouldn't that be first?

        Example:
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

        if not friendly:
            blueprint_string = (zlib.decompress(blueprint_string)
                                .decode('ascii'))
        
        # blueprint legend and layers are separated by blank lines
        # legend comes first, rest are layers
        blueprint_split = blueprint_string.split('\n\n')
        
        if friendly:
            legend_string = blueprint_split[0]
            blueprint_strings = blueprint_split[1:]
            
            # create a legend mapping of ascii symbol to tile graphic name
            legend = {}

            for line in legend_string.split('\n'):
                symbol, tile_name = line.split(' ', 1)  # e.g.: ` grass
                legend[symbol] = tile_name

        else:
            blueprint_strings = blueprint_split

        # transform our characters into a 3D list of tile graphic names
        layers = []

        for layer_string in blueprint_strings:
        
            if friendly:
                layer = [[legend[c] for c in row]
                         for row in layer_string.split('\n')]

            else:
                layer = [[name for name in row.split(';')]
                         for row in layer_string.split('\n')]

            layers.append(layer)

        return TileMap('debug', layers)


class TileSwatch(object):

    def __init__(self, swatch_name):
        """Named pygame.Surface instances of tiles in swatch directory.

        Note:
          Abstraction of a directory of images
          accompanied by a config file.

          INI defines default tile properties, default tile.

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
        self.info = {}
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

        for tile_name, flags in config_file.items('tileinfo_flags'):
            tileinfo = TileInfo(
                                tile_name,
                                flags=[f.strip() for f in flags.split(',')]
                               )
            self.info[tile_name] = tileinfo

        # set swatch images
        for full_file_name in glob.iglob(tile_pattern):
            file_name, file_ext = os.path.splitext(full_file_name)
            file_name = os.path.split(file_name)[1]
            tile_image = pygame.image.load(full_file_name)
            self.tile_size = tile_image.get_size()
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


class TileInfo(object):
    """Tile info/properties/attributes.

    Attributes:
      rect:
      flags: inherits flags of flags set on higher layers
      graphic_name:

    """

    def __init__(self, tile_graphic_name, flags=None):
        """Describe a tile.

        Args:
          tile_graphic_name (str): --
          flags (list|None): a list of strings, namely properties as
            seen above.

        """

        self.graphic_name = tile_graphic_name
        self.flags = set(flags) if flags else set()
        self.rect = None
        
    def __add__(self, other_tileinfo):
        self.flags.update(other_tileinfo.flags)
        
        if other_tileinfo.rect:
            self.rect = other_tileinfo.rect
