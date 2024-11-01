import os
import sys
from glob import glob

import pygame

from core.events.EventKeyboard import EventKeyboard
from core.events.EventMouse import EventMouse
from core.events.EventQuit import EventQuit
from core.render import Render
from core.scene import Scene
from core.Settings import Settings


class Game:
    def __init__(self, settings: Settings):
        self.__settings =  settings
        self.__game_loop = False
        self.__render = None
        self.__scenes = []
        self.__current_scene = None
        self.__clock = pygame.time.Clock()

    def load_scenes(self) -> bool:
        files_scenes = self.get_files("./" + self.__settings.name_project + self.__settings.path_scene)

        if len(files_scenes) == 0:
            print("Scenes not found while loading game; core.py:28")
            return False

        for scene_file in files_scenes:
            self.__scenes.append(Scene(scene_file))

    def get_render(self) -> Render:
        return self.__render

    def run(self):
        print("Init PyGame...")
        pygame.init()
        print("Load scenes...")
        self.load_scenes()

        print("Load objects from scene...")
        self.__current_scene = self.__scenes[0].load_objects()

        if self.__current_scene is None:
            print("Scene can't loaded while start game; core.py:44")
            return

        print("Init render...")
        if not pygame.image.get_extended():
            print("Your system not supported png and jpeg formats for images")
        self.__render = Render(self.__current_scene, self.__settings.width_window, self.__settings.height_window)

        print("Start game loop...")
        self.__game_loop = True
        self.game_loop()

    def game_loop(self):
        while self.__game_loop:
            self.__render.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__current_scene.on_event(EventQuit())
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEWHEEL or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
                    self.__current_scene.on_event(EventMouse(event))
                elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                    self.__current_scene.on_event(EventKeyboard(event))

            self.__current_scene.update_objects()

            self.__clock.tick(self.__settings.fps)

    @staticmethod
    def get_files(dir):
        return glob(os.path.join(dir, '*.json'))