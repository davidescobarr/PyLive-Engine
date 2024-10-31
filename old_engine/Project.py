import os
from glob import glob

from core.scene import Scene


class Project:
    def __init__(self, path_project):
        if path_project == '':
            raise Exception("Null project")

        self.__scene = None
        self.__objects = {}
        self.__scenes = []
        self.__path_project = path_project
        self.load_scenes()
        if len(self.__scenes) > 0:
            self.load_scene(self.__scenes[0])

    def load_scenes(self):
        files_scenes = self.get_files(self.__path_project + "/scene/")

        if len(files_scenes) == 0:
            print("Scenes not found while loading game; core.py:28")
            return False

        for scene_file in files_scenes:
            self.__scenes.append(Scene(scene_file))

    def load_scene(self, scene: Scene):
        self.__scene = scene
        self.__objects = self.__scene.get_scene_objects()['objects']

    def get_objects(self):
        return self.__objects

    @property
    def path_project(self):
        return self.__path_project

    @staticmethod
    def get_files(dir):
        return glob(os.path.join(dir, '*.json'))