import os
import json
import pygame
import random

from hypatia import class_default, class_get

@class_default
class Character(pygame.sprite.Sprite):
    SPRITE_TYPES = [
        "normal",
        "walk_north",
        "walk_south",
        "walk_east",
        "walk_west",
    ]

    def __init__(self, sprites):
        self.sprites = sprites
        self.active_sprite = "normal"

    @classmethod
    def from_resource_pack(cls, resourcepack, name):
        basepath = resourcepack.join("/sprites", name)
        sprites = {}

        for type in cls.SPRITE_TYPES:
            try:
                if resourcepack.exists(resourcepack.join(basepath, type + os.extsep + "gif")):
                    sprite = class_get("AnimatedSprite").from_resource_pack_gif(resourcepack, name, type)
                else:
                    sprite = class_get("AnimatedSprite").from_resource_pack_png(resourcepack, name, type)

                sprites[type] = sprite
            except:
                continue

        return cls(sprites)

    def update(self, timedelta):
        self.sprites[self.active_sprite].update(timedelta)
        self.image = self.sprites[self.active_sprite].image
        self.rect = self.sprites[self.active_sprite].rect

    def interact(self):
        return {}

    def __repr__(self):
        sprite_names = ",".join([a for a in self.sprites.keys()])
        return f"<{self.__class__.__name__} sprites=({sprite_names})>"

@class_default
class NPCCharacter(class_get("Character")):
    def __init__(self, npc_data, start_pos, movement_data, sprites):
        self.npc_data = npc_data
        self.start_pos = start_pos
        self.movement_data = movement_data

        self.current_pos = self.start_pos

        self.movement = False

        if self.movement_data is not None:
            self.movement = True

            if "move_every" in self.movement_data:
                self.move_every = self.movement_data["move_every"]

            if "move_for" in self.movement_data:
                self.move_for = self.movement_data["move_for"]

            if "rect" in self.movement_data:
                (left, top, width, height) = self.movement_data["rect"]
                self.movement_within_rect = pygame.Rect(left, top, width, height)

            self.time_since_last_movement = 0
            self.is_moving = False
            self.movement_direction = [0, 0]

        super().__init__(sprites)

    @classmethod
    def from_resource_pack(cls, resourcepack, name, mapdata):
        npcpath = resourcepack.join("/npcs", name + os.extsep + "json")

        npcdata = json.load(resourcepack.open(npcpath))

        spritebasepath = resourcepack.join("/sprites", npcdata["sprite"])
        sprites = {}

        for type in cls.SPRITE_TYPES:
            try:
                if resourcepack.exists(resourcepack.join(spritebasepath, type + os.extsep + "gif")):
                    sprite = class_get("AnimatedSprite").from_resource_pack_gif(resourcepack, npcdata["sprite"], type)
                else:
                    sprite = class_get("AnimatedSprite").from_resource_pack_png(resourcepack, npcdata["sprite"], type)

                sprites[type] = sprite
            except:
                continue

        return cls(npcdata, mapdata["start_pos"], mapdata["movement"] if "movement" in mapdata else None, sprites)

    def update(self, td):
        super().update(td)
        seconds = td / 1000.0

        if self.movement and not self.is_moving:
            self.time_since_last_movement += td 

            if self.time_since_last_movement >= self.move_every:
                self.is_moving = True
                self.time_since_last_movement = 0

                self.movement_direction = self.choose_movement_direction()

        elif self.movement and self.is_moving:
            self.time_since_last_movement += td

            if self.movement_direction[0] > 0:
                self.current_pos[0] += self.movement_data["move_speed"] * seconds
            elif self.movement_direction[0] < 0:
                self.current_pos[0] -= self.movement_data["move_speed"] * seconds

            if self.movement_direction[1] > 0:
                self.current_pos[1] += self.movement_data["move_speed"] * seconds
            elif self.movement_direction[1] < 0:
                self.current_pos[1] -= self.movement_data["move_speed"] * seconds

            if self.time_since_last_movement >= self.movement_data["move_for"]:
                self.is_moving = False
                self.time_since_last_movement = 0
                self.movement_direction = [0, 0]

    def choose_movement_direction(self):
        # figure out the movement direction
        rect = self.movement_within_rect.copy()
        rect.x = rect.x - self.start_pos[0]
        rect.y = rect.y - self.start_pos[1]

        relative_x = rect.center[0] 
        relative_y = rect.center[1]
        width = rect.width
        height = rect.height

        possible = []

        # if we're in the left-most quarter
        if relative_x >= width / 4:
            possible.append("right")

        # if we're in the right-most quarter
        elif relative_x <= (width / 4) * 3:
            possible.append("left")

        # outside the bounds on the right
        elif relative_x >= width:
            possible.append("left")

        # outside the bounds on the left
        elif relative_x - width < 0:
            possible.append("right")

        # in the middle
        else:
            possible.append("left")
            possible.append("right")

        # if we're in the top-most quarter
        if relative_y >= height / 4:
            possible.append("down")

        # if we're in the bottom-most quarter
        elif relative_y <= (height / 4) * 3:
            possible.append("up")

        # outside the bounds on the bottom
        elif relative_y >= height:
            possible.append("up")

        # outside the bounds on the top
        elif relative_y - height < 0:
            possible.append("down")

        else:
            possible.append("up")
            possible.append("down")

        if len(possible) > 0:
            direction = random.choice(possible)
        else:
            # this should never happen but put it in anyway
            direction = None

        if direction == "right":
            return [1, 0]

        elif direction == "left":
            return [-1, 0]

        elif direction == "down":
            return [0, 1]

        elif direction == "up":
            return [0, -1]

        else:
            return [0, 0]

    def interact(self):
        if self.npc_data["action"] == "say_lines":
            return {
                "say": self.npc_data["lines_to_say"],
            }
        else:
            return None

@class_default
class TileNPCCharacter(class_get("Character")):
    def __init__(self, tile_data):
        self.tile_data = tile_data
        self.tilesheet = self.tile_data["actual_tile"].tilesheet

        sprites = {"normal": self.tile_data["actual_tile"]}
        super().__init__(sprites)

    def is_solid(self):
        return self.tile_data["actual_tile"].is_solid()

    def is_destructible(self):
        return self.tile_data["actual_tile"].is_destructible()

    def is_animated(self):
        return self.tile_data["actual_tile"].is_animated()

    def interact(self):
        if class_get("TilemapTileFlags").STATIC_NPC in self.tile_data["flags"]: 
            return {
                "say": self.tile_data["metadata"]["lines_to_say"],
            }

        elif class_get("TilemapTileFlags").TELEPORTER in self.tile_data["flags"]:
            return {
                "teleport": {
                    "map": self.tile_data["metadata"]["teleport_map"],
                    "start_pos": self.tile_data["metadata"]["teleport_pos"] if "teleport_pos" in self.tile_data["metadata"] else None,
                }
            }

        elif class_get("TilemapTileFlags").CUSTOM_CODE in self.tile_data["flags"]:
            modpath, funcname = self.tile_data["metadata"]["function"].split(":")

            mod = __import__(modpath)

            for i in modpath.split(".")[1:]:
                mod = getattr(mod, i, None)
                if mod is None:
                    return None

            if not hasattr(mod, funcname):
                return None

            return getattr(mod, funcname)()

        return None
