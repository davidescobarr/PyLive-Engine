import threading
import os
import sys
from glob import glob

import pygame

from core.events.EventKeyboard import EventKeyboard
from core.events.EventMouse import EventMouse
from core.events.EventQuit import EventQuit
from core.Render import Render
from core.Scene import Scene
from core.Settings import Settings


class Game:
    def __init__(self, settings: Settings):
        self.__settings = settings
        self.__game_loop = False
        self.__render = None
        self.__scenes = []
        self.__current_scene = None
        self.__clock = pygame.time.Clock()

    def load_scenes(self) -> bool:
        """Load scene files based on settings and initialize Scene objects."""
        scenes_dir = self.__settings.folder + "/" + self.__settings.path_scene
        files_scenes = self.get_files(scenes_dir)

        if not files_scenes:
            print("Scenes not found while loading game; core.py:28")
            return False

        for scene_file in files_scenes:
            self.__scenes.append(Scene(scenes_dir, scene_file))
        return True

    def set_scene(self, scene: Scene):
        self.__current_scene = scene

    def get_render(self) -> Render:
        """Returns the render object."""
        return self.__render

    def run_in_other_thread(self):
        game_thread = threading.Thread(target=self.run)
        game_thread.start()

    def run(self, dev: bool = False):
        """Initialize PyGame, load scenes, and start the game loop."""
        print("Init PyGame...")
        pygame.init()
        pygame.display.set_caption(self.__settings.name_project)

        print("Load scenes...")
        if not self.load_scenes():
            return

        print("Load objects from scene...")
        if not self.__current_scene:
            self.__current_scene = self.__scenes[0].load_objects()

        if self.__current_scene is None:
            print("Scene can't be loaded; core.py:44")
            return

        print("Init render...")
        if not pygame.image.get_extended():
            print("Your system does not support PNG and JPEG formats for images")

        self.__render = Render(self.__current_scene, self.__settings.width_window, self.__settings.height_window)

        print("Start game loop...")
        self.__game_loop = True
        self.start_game_loop(dev)

    def stop(self):
        self.__game_loop = False
        pygame.quit()

    def start_game_loop(self, dev: bool = False):
        if dev:
            """Start the game loop in a separate thread."""
            game_thread = threading.Thread(target=self.game_loop)
            game_thread.start()
        else:
            self.game_loop()

    def game_loop(self):
        """Main game loop to process events, update objects, and render."""
        try:
            while self.__game_loop:
                self.__render.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__current_scene.on_event(EventQuit())
                        pygame.quit()
                        sys.exit()
                    elif event.type in (
                            pygame.MOUSEMOTION, pygame.MOUSEWHEEL, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                        self.__current_scene.on_event(EventMouse(event))
                    elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                        self.__current_scene.on_event(EventKeyboard(event))

                self.__current_scene.update_objects()
                self.__clock.tick(self.__settings.fps)
        except:
            print("Game crashed")
            self.stop()

    @staticmethod
    def get_files(directory):
        """Get a list of JSON files in the specified directory."""
        return glob(os.path.join(directory, '*.json'))