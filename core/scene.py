import json
import importlib.util
import sys

from core.events.Event import Event
from core.objects.Object import Object


class Scene:
    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path
        self.__objects = []

    def load_objects(self):
        with open(self.__file_path) as file:
            scene_file = json.load(file)

        if scene_file is None:
            print("scene.py:13 error while loading scene: scene file not found")
            return None

        self.load_group(scene_file['objects'])
        return self

    def load_object(self, object):
        properties = object['properties']
        object = self.load_class_from_file("example_project/" + properties['class'], properties['className'])
        if isinstance(object, Object):
            object.load_properties(properties)
            self.__objects.append(object)
        else:
            print("Class object not extends base class Object! scene.py:29")

    def load_group(self, group):
        for object in group:
            if object['type'] == "group":
                self.load_group(object['objects'])
            if object['type'] == "object":
                self.load_object(object)

    def get_objects(self):
        return self.__objects

    def update_objects(self):
        for object in self.__objects:
            object.update()

    def on_event(self, event: Event):
        for object in self.__objects:
            object.on_event(event)

    @staticmethod
    def load_class_from_file(file_path, class_name):
        spec = importlib.util.spec_from_file_location("module_name", file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["module_name"] = module
        spec.loader.exec_module(module)

        cls = getattr(module, class_name)
        return cls()