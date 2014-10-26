-- drop
DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS layers;
DROP TABLE IF EXISTS properties;
DROP TABLE IF EXISTS tile_properties;

-- create
CREATE TABLE settings (
    name TEXT,
    layer_width INTEGER,
    layer_height INTEGER,
    tile_width INTEGER,
    tile_height INTEGER
);

CREATE TABLE layers (
    id INTEGER PRIMARY KEY,
    -- pygame.image.tostring
    image_string TEXT
);

CREATE TABLE properties (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE tile_properties (
    tile_id INTEGER,
    property_id INTEGER,
    FOREIGN KEY (property_id) REFERENCES properties(id)
);
