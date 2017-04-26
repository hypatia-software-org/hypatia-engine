# Hypatia Engine 0.4.0 to-do list

## Core

- [x] Figure out game filesystem layout
- [x] User and game config separation
  - [x] Set custom keymaps in user config file
- [x] AnimatedSprite 
- [x] Tiles / Tilesheets
  - [x] Animated tiles
- [x] Tilemaps
  - [x] Player start position in map
  - [x] Tile metadata
    - [x] Setting tiles as objects
  - [x] Allow dumping tilemap back to it's source 
- [x] Moveable camera
  - [x] Centering on a given Rect
- [x] Resource packs
  - [x] Read resources from filesystem
  - [ ] Allow saving back to the filesystem
- [x] Importing of project code (in `lib/` directory)
- [x] In-game error handling
  - [ ] Add buttons from UI library
- [x] Make movement not tied to frame rate
- [ ] Add an unpoppable state at the bottom of the stack that displays an error message so that there is always at least 1 scene on the stack
- [ ] NPCs 
  - [x] Saying static lines
  - [x] Teleportation
  - [x] Running custom code on interaction
  - [x] Random character movement within given bounds
  - [ ] Add NPC current position to the collision rect checking
  - [ ] Allow the player to interact with NPCs
- [x] Allow games to override in-built classes with their own
- [ ] Inventory system
- [ ] UI description language
  - [ ] Buttons emit signals which are connected to with a `signal_connect("signal_name", callback)`
  - [ ] Allow recursive items (for example, displaying each item in inventory)
- [ ] Settings menu
  - [ ] Allow setting keymaps
- [ ] Savegame support
- [ ] Editor
  - [ ] Tilemap editing
  - [ ] NPC placement
  - [ ] Menu previewing (and possibly editing)

## Utilities

- [x] Tilesheet annotation script
- [x] Line wrapping utility
