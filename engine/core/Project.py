import json
import os
from glob import glob
from typing import List, Optional

from core.Scene import Scene
from core.Settings import Settings


class Project:
    def __init__(self, path_project: str, settings: Settings):
        self.__path = path_project
        self.__settings = settings

        self.__scenes = []
        self.__current_scene = None
        self.__notify_scene_change = None

    def init_scenes(self) -> List[Scene]:
        self.__scenes = []

        path_scenes = self.__path + "/" + self.__settings.path_scene

        files_scenes = glob(os.path.join(path_scenes, '*.json'))

        for file in files_scenes:
            self.__scenes.append(Scene(path_scenes, file))

        self.__scenes = sorted(self.__scenes,
            key=lambda scene: scene.order_load)

        for scene in self.__scenes:
            scene.order_load = self.__scenes.index(scene)

        print(f"{len(self.__scenes)} scenes was successfully loaded")
        return self.__scenes

    def reorder_scenes(self):
        self.__scenes = sorted(self.__scenes,
            key=lambda scene: scene.order_load)

    def delete_scene(self, scene: Scene):
        if scene in self.__scenes:
            self.__scenes.remove(scene)
            if self.__current_scene == scene:
                self.__current_scene = None
                if len(self.__scenes) != 0:
                    self.init_scene(self.__scenes[0], dev=True)
                else:
                    self.create_new_scene("scene")
                    self.init_scenes()
                    self.init_scene(self.__scenes[0], dev=True)

            scene.delete()

            if self.__notify_scene_change:
                self.__notify_scene_change()
            print(f"Scene was deleted")

    def init_scene(self, scene: Scene, dev: bool = False) -> None:
        scene.dev = dev
        scene.load_objects()
        self.__current_scene = scene
        if self.__notify_scene_change:
            self.__notify_scene_change()
        print(f"Scene was loaded")

    def set_notify_for_change_scene(self, notify: callable):
        self.__notify_scene_change = notify

    def create_new_scene(self, name: str):
        scene = Scene.default_structure(name, len(self.__scenes))
        path_scene = self.__path + "/" + self.__settings.path_scene + name + ".json"

        with open(path_scene, 'w') as file:
            json.dump(scene, file)

        self.__scenes.append(Scene(self.__path + "/" + self.__settings.path_scene, path_scene))

    def get_scenes(self) -> List[Scene]:
        return self.__scenes

    def get_scene_by_name(self, name: str) -> Optional[Scene | None]:
        for scene in self.__scenes:
            if scene.name == name:
                return scene
        return None

    def get_current_scene(self) -> Scene:
        return self.__current_scene

    @property
    def path_project(self):
        return self.__path

    @property
    def settings(self) -> Settings:
        return self.__settings