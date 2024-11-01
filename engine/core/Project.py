import os
from glob import glob
from typing import List

from core.scene import Scene
from core.settings import Settings


class Project:
    def __init__(self, path_project: str, settings: Settings):
        self.__path = path_project
        self.__settings = settings

        self.__scenes = []
        self.__current_scene = None

    def init_project(self):
        pass

    def init_scenes(self) -> List[Scene]:
        path_scenes = self.__path + "/" + self.__settings.path_scene

        files_scenes = glob(os.path.join(path_scenes, '*.json'))

        for file in files_scenes:
            self.__scenes.append(Scene(file))

        print(f"{len(self.__scenes)} scenes was successfully loaded")
        return self.__scenes

    def init_current_scene(self, scene: Scene) -> None:
        scene.load_objects()
        self.__current_scene = scene
        print(f"Scene was loaded")

    def create_new_scene(self, name: str):
        pass

    def get_scenes(self) -> List[Scene]:
        return self.__scenes

    def get_current_scene(self) -> Scene:
        return self.__current_scene

    @property
    def settings(self) -> Settings:
        return self.__settings