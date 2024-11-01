import json
from typing import Optional

from core.events.Event import Event
from core.objects.Object import Object
from core.scene.components.Group import Group
from core.scene.components.Object import SceneObject
from core.utils.ClassLoader import load_class_from_file


class Scene:
    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path
        self.__path_project = file_path + "/../"
        self.__objects = []
        self.hierarchy_objects = []
        self.__main_group = None
        self.__name = self.get_scene_objects()["name"]

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    def get_scene_file(self):
        return self.__file_path

    def get_scene_objects(self):
        with open(self.__file_path) as file:
            scene_file = json.load(file)
        return scene_file

    def load_objects(self):
        scene_file = self.get_scene_objects()

        if scene_file is None:
            print("scene.py:13 error while loading scene: scene file not found")
            return None

        self.__main_group = self.load_group(scene_file['objects'])
        return self

    def load_object(self, object) -> Optional[SceneObject | None]:
        properties = object['properties']
        object = load_class_from_file(self.__path_project + properties['class'], properties['className'])
        if isinstance(object, Object):
            object.load_properties(properties)
            self.__objects.append(object)
            return SceneObject(self, object)
        else:
            print("Class object not extends base class Object! scene.py:29")

        return None

    def load_group(self, group) -> Group:
        scene_group = Group(self, group["name"])

        for object in group:
            if object['type'] == "group":
                scene_group.add_object(self.load_group(object['objects']))
            if object['type'] == "object":
                scene_group.add_object(self.load_object(object))

        return scene_group

    def get_objects(self):
        return self.__objects

    def update_objects(self):
        for object in self.__objects:
            object.update()

    def on_event(self, event: Event):
        for object in self.__objects:
            object.on_event(event)

    def save(self):
        scene = {
            "name": self.__name,
            "objects": [self.__main_group.to_dict()]
        }

        with open(self.__file_path, 'w') as file:
            json.dump(file, scene)