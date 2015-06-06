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
import zipfile
import itertools
from StringIO import StringIO

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


# bad?
coord_to_index = lambda width, x, y: (width * y) + x


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
      npcs:

    """

    def __init__(self, tilesheet_name, tile_ids, npcs=None):
        """Stitch tiles from swatch to layer surfaces. 

        Piece together layers/surfaces from corresponding tile graphic
        names, using the specified tile swatch. Keep track of
        metadata, including passability.

        Args:
          tilesheet_name (str): directory name of the swatch to use
          tile_ids (list): 3d list where list[layer][row][tile]
          npcs (list): list of player.Npc objects

        Examples:
          Make a 2x2x1 tilemap:
          >>> tiles = [[0, 0], [0, 0]]
          >>> tilemap = TileMap('debug', tiles)

        Note:
          Maybe this shouldn't hold npcs!

        """

        # create the layer images and tile properties
        tilesheet = TileSheet.from_name(tilesheet_name)
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

        for z, layer in enumerate(tile_ids):
            new_layer = pygame.Surface(layer_size, pygame.SRCALPHA, 32)
            new_layer.fill([0,0,0,0])
        
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
                    if tile.id == -1:
                    
                        continue
                    
                    # blit tile subsurface onto respective layer
                    tile_position = (x * tile_width, y * tile_height)
                    new_layer.blit(tile.subsurface, tile_position)
                    
                    # finally passability!
                    if 'impass_all' in tile.flags:
                        impassable_rects.append(pygame.Rect(tile_position,
                                                            tile_size))
                    
            layer_images.append(new_layer)

        self.tilesheet = tilesheet
        self.layer_images = layer_images
        self.tiles = tiles
        self.impassable_rects = impassable_rects
        self.dimensions_in_tiles = dimensions_in_tiles
        self.npcs = npcs
        self._tile_ids = tile_ids
        
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

    def to_string(self, separator=' '):
        """Create the user-unfriendly string for the tilemap.
        
        Args:
          separator (str): can be ''
          
        """

        output_string = ''
                    
        # create map layers
        layers = []
        
        for layer in self._tile_ids:
            layer_lines = []
        
            for row in layer:
                row_string = separator.join([str(i) for i in row])
                    
                layer_lines.append(row_string)
                    
            layer_string = '\n'.join(layer_lines)
            layers.append(layer_string)

        layers_string = '\n\n'.join(layers)
        output_string += layers_string

        return output_string

    @classmethod
    def from_string(cls, blueprint_string, separator=' '):
        """This is a debug feature. Create a 3D list of tile names using
        ASCII symbols. Supports layers.
       
        Note:
          In the future, there will be more "positionals" which follow
          the legend block, e.g., npcs, which would then be followed by
          all of the layers.
          
          What about swatch name? Shouldn't that be first?
          
        """
        
        # blueprint legend and layers are separated by blank lines
        # legend comes first, rest are layers
        blueprint_split = blueprint_string.split('\n\n')
        
        # in the future the first few elements of blueprint_split
        # will have some sort of meta
        blueprint_strings = blueprint_split

        # transform our characters into a 3D list of tile graphic names
        layers = []

        for layer_string in blueprint_strings:
            layer = [[int(tile_id) for tile_id in row.split(separator)]
                     for row in layer_string.split('\n')]
            layers.append(layer)

        return TileMap('debug', layers)


class TileSheet(object):

    def __init__(self, surface, tiles):
        self.surface = surface
        self.tiles = tiles

    def __getitem__(self, tile_id):

        try:

            return self.tiles[tile_id]

        except KeyError:

            raise BadTileName(self.name, tile_id)

    @classmethod
    def from_name(self, tilesheet_name):
        """Create a TileSheet from a name, corresponding to a path
        pointing to a tilesheet zip archive.
        
        Args:
          tilesheet_name (str): this string is appended to the default
            resources/tilesheets location.
        
        Returns:
          TileSheet: initialized utilizing information from the
            respective tilesheet zip's tilesheet.png and tilesheet.ini.
          
        """
        
        # path to the zip containing tilesheet.png and tilesheet.ini
        zip_path = os.path.join(
                                'resources',
                                'tilesheets',
                                tilesheet_name + '.zip'
                               )

        with zipfile.ZipFile(zip_path) as zip:
            zip_png = zip.open('tilesheet.png').read()
            config_file = zip.open('tilesheet.ini').read()
        
        png_io = StringIO(zip_png)
        tilesheet_surface = pygame.image.load(png_io)
        config_io = StringIO(config_file)
        config = configparser.ConfigParser()
        config.readfp(config_io)
        
        flags = {int(k): set(v.split(',')) for k, v in config.items('flags')}
        tile_width = config.getint('meta', 'tile_width')
        tile_height = config.getint('meta', 'tile_height')
        tile_size = (tile_width, tile_height)
        tilesheet_width, tilesheet_height = tilesheet_surface.get_size()
        
        x_positions = xrange(0, tilesheet_width, tile_width)
        y_positions = xrange(0, tilesheet_height, tile_height)
        topleft_positions = []
        
        for y in y_positions:
        
            for x in x_positions:
                topleft_positions.append((x, y))
                
        tiles = []
        
        for tile_id, top_left in enumerate(topleft_positions):
            tile = Tile(
                        tile_id=tile_id,
                        surface=tilesheet_surface,
                        tile_size=tile_size,
                        subsurface_position=top_left,
                        flags=flags.get(tile_id, None)
                       )
            tiles.append(tile)

        return TileSheet(tilesheet_surface, tiles)


class Tile(object):
    """
    
    Attributes:
      --
    
    """

    def __init__(self, tile_id, surface, tile_size,
                 subsurface_position, flags=None):
        """create subsurface of tilesheet surface using topleft
        position on tilesheet.

        Args:
          tile_id (int): --
          surface (pygame.Surface): tilesheet surface
          tile_size (tuple): x, y dimensions of tiles in pixels
          subsurface_position: the topleft coordinate of the tile
            relative to the topleft of surface.
          flags (set): properties belonging to this tile

        """
        
        position_rect = pygame.Rect(subsurface_position, tile_size)
        self.subsurface = surface.subsurface(position_rect)
        self.flags = flags or set()
        self.rect = pygame.Rect((0, 0), tile_size)
        self.id = tile_id
        self.size = tile_size

