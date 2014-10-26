# engine/tiles.py
# Lillian Lynn Mahoney <lillian.lynn.mahoney@gmail.com>
#
# This module is part of Untitled Game Engine and is released under the
# Attribution Assurance License: http://opensource.org/licenses/AAL

"""tile-based map management.

Using "paint by number" as an analogy:
  * TileMap is the canvas/picture with number cells (the canvas)
  * TileSwatch defines what those numbers correspond to
    (the paint palettte)

Each tile of the first layer in a TileMap has its respective
TileProperties object. Every tile in a TileSwatch has default
properties defined in its swatch.ini.

For more info: http://en.wikipedia.org/wiki/Tile_engine

"""

import os
import glob
import string
import pygame
import sqlite3
import cStringIO
import ConfigParser


__author__ = "Lillian Lynn Mahoney"
__copyright__ = "Copyright 2014, Lillian Lynn Mahoney"
__credits__ = ["Lillian Mahoney"]
__license__ = "Attribution Assurance License"
__version__ = "0.3.1"
__maintainer__ = "Lillian Mahoney"
__email__ = "lillian.lynn.mahoney@gmail.com"
__status__ = "Development"


NEW_SCENE_TILES_WIDE = 10
NEW_SCENE_TILES_TALL = 10
NEW_SCENE_SWATCH = 'debug'


class BadTileName(Exception):
    """KeyError raised when searching for key in the TileSwatch's
    {name: image} dictionary.

    No tile by name %(key)s.

    """

    def __init__(self, swatch_name, key):
        message = ('TileSwatch: no tile by name "%s"'  % (key, swatch_name))
        Exception.__init__(self, message)


class MissingLayerMethod(Exception):
    """Occurs when the user does not provide image_layers or
    make_layers + swatch.

    """

    def __init__(self):
        message = ('TileMap requries image_layers OR make_layers + swatch')
        Exception.__init__(self, message)


class TileMap(object):

    def __init__(self, name,
                 image_layers=None, tile_size=None,
                 make_layers=None, swatch=None,
                 properties=None):
        """Tile (cell) based map. Each tile of the first layer has
        TileProperties, which you can reference by pixel or tile
        coordinate.

        You can either provide the layer images as a list of pygame
        surfaces (image_layers), or you can provide a 2D list of tile
        names/strings (make_layers) and a TileSwatch, which defines
        said names (swatch).

        Args:
          name (str): will be used for sqlite db and other things

          image_layers (list|None): 1D list of pygame.Surface objects
            to use as the TileMap's graphical layers.
          tile_size (tuple|None): (x, y) in pixels, ONLY USE IF USING
            image_layers!
 
          make_layers (list|None): list of 2D lists, whose elements
            are strings referencing a corresponding TileSwatch
            tile name.
          swatch (TileSwatch|None): TileSwatch which defines the
            tile names used in tiles arg. ONLY USE IF USING make_layers!

          properties (list|None): list of TileProperties (cascade over
            defaults)

        Planned Features:
          * plans to implement paralax--effect applied to tilemap.bg
            or tilemap.fg?

        """

        if make_layers and swatch:
            first_layer = make_layers[0]
            tile_size = swatch.tile_size
            size = (len(first_layer[0]), len(first_layer), len(make_layers))

            layer_width = len(first_layer[0]) * tile_size[0]
            layer_height = len(first_layer) * tile_size[1]
            layer_size = (layer_width, layer_height)

            # properties
            properties = [swatch.properties[x] for y in first_layer for x in y]

            # layer first
            layers = []

            for z, layer in enumerate(make_layers):
                new_layer = pygame.Surface(layer_size)

                for y, row in enumerate(layer):

                    for x, tile in enumerate(row):
                        tile_position = (x * swatch.tile_size[0],
                                         y * swatch.tile_size[1])
                        new_layer.blit(swatch[tile], tile_position)

                layers.append(new_layer)
                tile_size = swatch.tile_size
                size = (len(layer), len(layer[0]))

        elif image_layers:
            layers = image_layers
            layers_x, layers_y = layers[0].get_size()
            tile_width, tile_height = tile_size
            size = (layers_x / tile_width, layers_y / tile_height)

        else:

            raise MissingLayerMethod()

        self.name = name
        self.layers = layers
        self.size = size
        self.tile_size = tile_size
        self.properties = properties

    def __getitem__(self, coord):
        """Fetch TileProperties by tile coordinate.

        Args:
          coord (tuple): (x, y) coordinate; z always just
            z-index (it's not a pixel value)

        Returns:
          TileProperties

        """

        x, y = coord
        height, width = self.size

        return self.properties[width * y + x]

    def get_properties(self, coord, unit_pixel=False):
        """Fetch TileProperties by tile or pixel coordinate.

        Args:
          coord (tuple): (x, y) coordinate; z always just
            z-index (it's not a pixel value)
          unit_pixel (bool): if True, unit values in coordinate
            are pixels, not tiles

        Returns:
          TileProperties

        """

        x, y = coord

        if unit_pixel:
            x = pixel_x / self.tile_size[0]
            y = pixel_y / self.tile_size[1]

        height, width = self.size

        return self.properties[width * y + x]


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

    def __init__(self, properties=None):
        """List of properties.

        Primarly scaffolding.

        Supported properties:
          * impass_north
          * impass_east
          * impass_south
          * impass_west
          * need_boat
          * harm_tile

        Args:
          properties (list): a list of strings, namely properties as
            seen above.

        Examples:
          >>> tile_properties = TileProperties(['teleport', 'sticky'])
          >>> "teleport" in tile_properties
          True
          >>> [p for p in tile_properties]
          ['teleport', 'sticky']

        """

        if properties:
            self.properties = frozenset(properties)
        else:
            self.properties = frozenset()

    def __iter__(self):

        return iter(self.properties)

    def __contains__(self, item):

        return item in self.properties


def save_tilemap(tilemap):
    """Pickle TileMap object to SQLITE database.

    Args:
      tilemap (TileMap): tilemap to save

    Returns:
      None

    """

    # Connect to database, reset database (start fresh)
    connection, cursor = tilemap_connect(tilemap.name)

    with open('sql/tilemap-setup.sql') as sql_file:
        cursor.executescript(sql_file.read())

    connection.commit()

    # insert a bunch of settings
    sql = '''
          INSERT INTO
              settings (
                  name,
                  layer_width,
                  layer_height,
                  tile_width,
                  tile_height
              )
          VALUES
              (?, ?, ?, ?, ?)
          '''
    params = (
              tilemap.name,
              tilemap.layers[0].get_size()[0],
              tilemap.layers[0].get_size()[1],
              tilemap.tile_size[0],
              tilemap.tile_size[1]
             )
    cursor.execute(sql, params)

    # save layers as string with pygame
    for layer in tilemap.layers:
        layer_as_string = pygame.image.tostring(layer, 'RGBA')
        sql = 'INSERT INTO layers (image_string) VALUES (?)'
        cursor.execute(sql, (layer_as_string,))

    # save tileproperties
    for tile_id, tile_properties in enumerate(tilemap.properties):
        property_ids = []

        for flag in tile_properties:

            try:
                sql = 'INSERT INTO properties (name) VALUES (?)'
                cursor.execute(sql, (flag,))
                property_id = cursor.lastrowid

            except sqlite3.IntegrityError:
                sql = 'SELECT id FROM properties WHERE name=?'
                cursor.execute(sql, (flag,))
                property_id = cursor.fetchone()[0]

            property_ids.append(property_id)

        for property_id in property_ids:
            sql = '''
                  INSERT INTO
                      tile_properties (
                          tile_id,
                          property_id
                      )
                  VALUES
                      (?, ?)
                  '''
            cursor.execute(sql, (tile_id, property_id,))

    connection.commit()
    connection.close()

    return None


def load_tilemap(tilemap_name):
    """Configure a TileMap object based on specified tilemap name's
    files.

    Args:
      tilemap_name (str): directory name containing desired configs and
        image files.

    Returns:
      TileMap: as defined from an SQLITE3 database. See: save_tilemap.

    """

    # settings first
    connection, cursor = tilemap_connect(tilemap_name)
    sql = 'SELECT * FROM settings'
    cursor.execute(sql)
    setting_names = ('name', 'layer_width', 'layer_height', 'tile_width',
                     'tile_height')
    settings = dict(zip(setting_names, cursor.fetchone()))
    tilemap_name = settings['name']
    layer_width = settings['layer_width']
    layer_height = settings['layer_height']
    layer_size = (layer_width, layer_height)
    tile_width = settings['tile_width']
    tile_height = settings['tile_height']
    tiles_wide = layer_width / tile_width
    tiles_tall = layer_height / tile_height

    # layers
    cursor.execute('SELECT image_string FROM layers ORDER BY id')
    image_text_layers = [row[0] for row in cursor.fetchall()]
    layers = []

    for image_text in image_text_layers:
        image = pygame.image.fromstring(image_text, layer_size, 'RGBA')
        layers.append(image)

    properties = []

    for i in xrange(tiles_wide * tiles_tall):
        sql = '''
              SELECT
                  properties.name
              FROM
                  tile_properties
              JOIN
                  properties on tile_properties.property_id = properties.id
              WHERE
                  tile_properties.tile_id=?
              ORDER BY
                  tile_properties.tile_id
              '''
        cursor.execute(sql, (i,))
        tile_properties = [row[0] for row in cursor.fetchall()]
        tiles_properties = TileProperties(tile_properties)
        properties.append(tile_properties)

    tilemap = TileMap(
                      name=tilemap_name,
                      image_layers=layers,
                      properties=properties,
                      tile_size=(tile_width, tile_height)
                     )

    return tilemap


def tilemap_connect(tilemap_name):
    """connect to tilemap db by opening related db

    sanitizes file/tilemap_name

    Args:
      tilemap_name (str): name of map (for humans) used for db file name

    Returns:
      tuple: sqlite.Connection, sqlite.Cursor

    """

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    tilemap_file_name = ''.join(c for c in tilemap_name if c in valid_chars)
    tilemap_file_name = tilemap_name + '.db'
    tilemap_db_path = os.path.join('data', 'tiles', 'maps', tilemap_file_name)
    connection = sqlite3.connect(tilemap_db_path)
    connection.text_factory = str

    return connection, connection.cursor()


def new_tilemap(tilemap_name):
    """Creates a new sqlite database, i.e., scene.

    Uses scene_name for file name and scene's label.

    Args:
      tilemap_name (str): name of map and sqlite db file.

    Returns:
        TileMap: empty/blank TileMap, one layer of default tile

    """


    # create default layer
    layer = []

    for y in xrange(NEW_SCENE_TILES_TALL):
        row = ['default' for x in xrange(NEW_SCENE_TILES_WIDE)]
        layer.append(row)

    layer[0][0] = 'water'
    layers = [layer]
    tilemap = TileMap(
                      name=tilemap_name,
                      make_layers=layers,
                      swatch=TileSwatch(NEW_SCENE_SWATCH),
                     )
    save_tilemap(tilemap)

    return tilemap


# debugging purposes
if __name__ == '__main__':
    import doctest
    doctest.testmod()

