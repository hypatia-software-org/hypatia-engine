import os
import sys
import json
import pygame
import traceback
import importlib.util

from hypatia import class_get, class_default
from hypatia.default_config import default_game_config, default_user_config

@class_default
class Game:
    def __init__(self, path, patch_builtins=True):
        self.path = path
        with open(os.path.join(path, "config.json"), 'r') as fh:
            self.gameconfig = json.load(fh)

        self.gamename = self.gameconfig['name']
        self.gamefriendlyname = self.gameconfig['friendly_name']

        self.import_modules_from_game_dir()

        if 'user_config_path' in self.gameconfig:
            user_config_path = self.gameconfig['user_config_path']

        else:
            try:
                xdg_config_path = os.environ["XDG_CONFIG_PATH"]
            except:
                xdg_config_path = os.path.expanduser("~/.config/")

            user_config_path = os.path.join(xdg_config_path, self.gamename, "config.json")

        if os.path.exists(user_config_path):
            with open(user_config_path, "r") as fh:
                self.userconfig = json.load(fh)

        else:
            if 'user_config' in self.gameconfig:
                self.userconfig = self.gameconfig['user_config']
            else:
                self.userconfig = default_user_config

            if not os.path.exists(os.path.dirname(user_config_path)):
                os.makedirs(os.path.dirname(user_config_path), exist_ok=True)

            with open(user_config_path, 'w') as fh:
                json.dump(self.userconfig, fh, sort_keys=True, indent=4)

        self.resourcepack = class_get("FilesystemResourcePack")(os.path.join(path, "resources"))

        self.clock = pygame.time.Clock()

        self.running = False
        self.scene_stack = []

    def scene_push(self, scenecls, *args, **kwargs):
        self.scene_stack.append(scenecls(self, *args, **kwargs))

    def scene_pop(self):
        self.scene_stack.pop()

    def scene_replace(self, scenecls, *args, **kwargs):
        self.scene_stack = []
        self.scene_push(scenecls, *args, **kwargs)

    def import_modules_from_game_dir(self):
        basepath = os.path.join(self.path, "lib")
        for root, dirs, files in os.walk(basepath):
            path = root[len(basepath):]
            if path.startswith("/"):
                path = path[1:]

            module_path_ary = [self.gamename]
            for i in path.split(os.sep):
                if i is not "":
                    module_path_ary.append(i)

            files_sorted = files
            if "__init__.py" in files:
                index = files.index("__init__.py")
                files_sorted.pop(index)
                files_sorted.insert(0, "__init__.py")

            for filename in files_sorted:
                new_module_path_ary = []

                if not filename.endswith(".py"):
                    continue

                if filename == "__init__.py":
                    new_module_path_ary = module_path_ary
                    module_path = ".".join(new_module_path_ary)
                else:
                    module_name = os.path.splitext(filename)[0]
                    new_module_path_ary = module_path_ary + [module_name]
                    module_path = ".".join(new_module_path_ary)

                # load the module
                abspath = os.path.join(os.path.abspath(root), filename)
                spec = importlib.util.spec_from_file_location(module_path, abspath)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

                # add the module to sys.modules so it's importable by other pieces of code
                sys.modules[module_path] = mod

                # if this module has a parent, add an attr to it with the new module
                if len(new_module_path_ary) > 1:
                    parent = sys.modules[".".join(new_module_path_ary[:-1])]
                    setattr(parent, module_name, mod)


    def run(self):
        pygame.init()

        if self.gameconfig["font_face"] != "default":
            font_obj = self.resourcepack.open(self.resourcepack.join("/fonts", self.gameconfig["font_face"]))
        else:
            font_obj = None

        self.font = pygame.font.Font(font_obj, int(self.gameconfig['font_size']))

        self.running = True

        if self.userconfig['display']['fullscreen']:
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(self.userconfig['display']['window_size'])

        self.scene_push(class_get("TilemapScene"), self.resourcepack, self.gameconfig['starting_tilemap'], self.gameconfig["player_character"])

        while self.running:
            self.display.fill((0, 0, 0))

            # update current scene
            try:
                self.scene_stack[-1].update()
            except Exception as ex:
                if isinstance(self.scene_stack[-1], class_get("TracebackScene")):
                    raise

                tb = traceback.format_exc()
                self.scene_push(class_get("TracebackScene"), ex, tb)
                print(tb)
                continue

            self.display.blit(self.scene_stack[-1].surface, (0, 0))

            # handle events
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.running = False

                try:
                    self.scene_stack[-1].handle_event(ev)
                except Exception as ex:
                    if isinstance(self.scene_stack[-1], class_get("TracebackScene")):
                        raise

                    tb = traceback.format_exc()
                    self.scene_push(class_get("TracebackScene"), ex, tb)
                    print(tb)
                    continue

            # display FPS if it's asked for
            if 'fpsdisplay' in self.userconfig['display'] and self.userconfig['display']['fpsdisplay'] is True:
                fps = self.clock.get_fps()
                text = self.font.render("%.02f FPS" % fps, True, (255, 255, 255))
                self.display.blit(text, (0, 0))

            # clock tick
            if 'fpslimit' in self.userconfig['display']:
                if self.userconfig['display']['fpslimit'] > 0:
                    fpslimit = self.userconfig['display']['fpslimit']
                else:
                    fpslimit = 60
            else:
                fpslimit = 60

            self.clock.tick(fpslimit)
            pygame.display.flip()