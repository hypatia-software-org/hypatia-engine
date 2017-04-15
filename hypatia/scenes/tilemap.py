import pygame

from hypatia import class_get, class_default
from hypatia.utils import keyname_to_keysym


@class_default
class TilemapScene(class_get("Scene")):
    def __init__(self, game, resourcepack, mapname, playername, start_pos=None):
        super().__init__(game)

        self.resourcepack = resourcepack
        self.player_name = playername

        self.tilemap = class_get("Tilemap").from_resource_pack(resourcepack, mapname)

        self.camera = class_get("Camera")(
            (self.tilemap.width, self.tilemap.height),
            self.game.gameconfig["camera_resolution"],
            self.game.display.get_size()
        )

        self.player = class_get("Character").from_resource_pack(resourcepack, playername)

        if start_pos is None:
            start_pos = self.tilemap.player_data["start_pos"]

        self.player_pos = [
            start_pos[0] * self.tilemap.tile_width,
            start_pos[1] * self.tilemap.tile_height
        ]

        self.movement_speed = self.game.gameconfig["movement_speed"]
        self.player_movement_speed = [0, 0]
        self.direction_facing = "north"

    def update(self):
        self.create_surface()
        self.camera.source_surface.fill((0, 0, 0))

        td = self.game.clock.get_time()
        self.player.update(td)

        seconds = td / 1000.0

        old_player_pos = self.player_pos.copy()

        if self.player_movement_speed[0] > 0:
            self.player_pos[0] += self.movement_speed * seconds
        elif self.player_movement_speed[0] < 0:
            self.player_pos[0] -= self.movement_speed * seconds

        if self.player_movement_speed[1] > 0:
            self.player_pos[1] += self.movement_speed * seconds
        elif self.player_movement_speed[1] < 0:
            self.player_pos[1] -= self.movement_speed * seconds

        if self.check_hitting_anything():
            self.player_pos = old_player_pos

        layers = self.tilemap.update(td)

        layers[int(self.tilemap.player_data["layer"])].blit(self.player.image, self.player_pos)

        for layer in layers:
            self.camera.source_surface.blit(layer, (0, 0))

        player_rect = pygame.Rect(self.player_pos, self.player.image.get_size())
        self.camera.center_on(player_rect)

        self.camera.update()

        self.surface.blit(self.camera, (0, 0))

    def check_hitting_anything(self):
        current_rect = pygame.Rect(self.player_pos, self.player.image.get_size())
        solid_blocks = self.tilemap.get_solid_rects()

        return current_rect.collidelist(solid_blocks) >= 0

    def interact_with_object(self):
        # determine the tile we're on
        tile_x = -1
        tile_y = -1
        for row_idx in range(0, self.tilemap.width_in_tiles):
            for column_idx in range(0, self.tilemap.height_in_tiles):
                tile_rect = pygame.Rect(column_idx * self.tilemap.tile_width, row_idx * self.tilemap.tile_height, self.tilemap.tile_width, self.tilemap.tile_height)
                player_rect = pygame.Rect(self.player_pos, self.player.image.get_size())
                if tile_rect.collidepoint(player_rect.center):
                    # this is our tile
                    tile_x = column_idx
                    tile_y = row_idx
                    break

        if tile_x == -1 or tile_y == -1:
            return

        # determine the tile we're facing
        if self.direction_facing == "north":
            if tile_y == 0:
                return

            tile = self.tilemap.tile_data[0][tile_y - 1][tile_x]

        elif self.direction_facing == "south":
            if tile_y + 1 == len(self.tilemap.tile_data[0]):
                return

            tile = self.tilemap.tile_data[0][tile_y + 1][tile_x]

        elif self.direction_facing == "west":
            if tile_x == 0:
                return

            tile = self.tilemap.tile_data[0][tile_y][tile_x - 1]

        elif self.direction_facing == "east":
            if tile_x + 1 == len(self.tilemap.tile_data[0][0]):
                return

            tile = self.tilemap.tile_data[0][tile_y][tile_x + 1]

        if hasattr(tile["tile"], "interact"):
            output = tile["tile"].interact()
            if output is None:
                return

            if "say" in output:
                self.game.scene_push(class_get("TextBoxScene"), output["say"])

            elif "teleport" in output:
                mapname = output["teleport"]["map"]
                startpos = output["teleport"]["start_pos"]

                self.game.scene_push(self.__class__, self.resourcepack, mapname, self.player_name, start_pos=startpos)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == keyname_to_keysym(self.game.userconfig["keymaps"]["forward"]):
                self.player_movement_speed[1] = -1
                self.direction_facing = "north"

            elif event.key == keyname_to_keysym(self.game.userconfig["keymaps"]["back"]):
                self.player_movement_speed[1] = 1
                self.direction_facing = "south"

            elif event.key == keyname_to_keysym(self.game.userconfig["keymaps"]["right"]):
                self.player_movement_speed[0] = 1
                self.direction_facing = "east"

            elif event.key == keyname_to_keysym(self.game.userconfig["keymaps"]["left"]):
                self.player_movement_speed[0] = -1
                self.direction_facing = "west"

            elif event.key == keyname_to_keysym(self.game.userconfig["keymaps"]["interact"]):
                self.interact_with_object()

        elif event.type == pygame.KEYUP:
            if event.key == keyname_to_keysym(self.game.userconfig["keymaps"]["forward"]):
                self.player_movement_speed[1] = 0

            elif event.key == keyname_to_keysym(self.game.userconfig["keymaps"]["back"]):
                self.player_movement_speed[1] = 0

            elif event.key == keyname_to_keysym(self.game.userconfig["keymaps"]["right"]):
                self.player_movement_speed[0] = 0

            elif event.key == keyname_to_keysym(self.game.userconfig["keymaps"]["left"]):
                self.player_movement_speed[0] = 0
