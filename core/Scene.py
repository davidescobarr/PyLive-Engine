import json
import os
from typing import Optional

from core.events.Event import Event
from core.objects.Object import Object
from core.scene.components.Group import Group
from core.scene.components.Object import SceneObject
from core.utils.ClassLoader import load_class_from_file
from core.utils.delegates.PropertyValueDelegate import DelegateNotifier


class Scene:
    def __init__(self, path, file_path: str) -> None:
        self.__file_path = file_path
        self.__path_project = path + "/../"
        self.__objects = []
        self.hierarchy_objects = []
        self.__main_group = None
        self.__order_load = 0
        scene_objects = self.get_scene_objects()
        self.__name = scene_objects["name"]
        if scene_objects.__contains__("order_load"):
            self.__order_load = scene_objects['order_load']
        self.__dev = False

        self.__notify_change_name = DelegateNotifier()

    def set_notify_for_change_name(self, notify: callable):
        self.__notify_change_name.subscribe(notify)

    @property
    def order_load(self):
        return self.__order_load

    @order_load.setter
    def order_load(self, value: int):
        if value < 0:
            value = 0
        self.__order_load = value

    @property
    def dev(self) -> bool:
        return self.__dev

    @dev.setter
    def dev(self, value: bool):
        self.__dev = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name
        self.__notify_change_name.notify()

    @property
    def main_group(self) -> Group:
        return self.__main_group

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

        self.__objects = []
        self.__main_group = self.load_group(scene_file['objects'], 0, "main_group")
        return self

    def load_object(self, object: Object, order: int) -> Optional[SceneObject | None]:
        properties = object['properties']
        name = object['name']
        load_object = load_class_from_file(properties['class'], properties['className'])
        if isinstance(load_object, Object) or load_object.__class__.__name__ == properties['className']:
            load_object.name = name
            load_object.load_properties(properties)
            self.__objects.append(load_object)
            return SceneObject(self, load_object, order)
        else:
            print("Class object not extends base class Object! scene.py:60")

        return None

    def load_group(self, group, order: int, name: str) -> Group:
        scene_group = Group(self, name, order)

        order = 0
        for object in group:
            if object['type'] == "group":
                scene_group.add_object(self.load_group(object['objects'], order, object['name']))
            if object['type'] == "object":
                load_object = self.load_object(object, order)
                if load_object:
                    scene_group.add_object(load_object)
                else:
                    continue

            order += 1

        return scene_group

    def get_objects(self):
        return self.__objects

    def update(self):
        pass

    def update_objects(self):
        if not self.__dev:
            for object in self.__objects:
                object.update()

    def on_event(self, event: Event):
        for object in self.__objects:
            object.on_event(event)

    def save(self):
        scene = Scene.default_structure(self.name, self.__order_load)
        main_group = self.__main_group
        if self.__main_group is None:
            scene['objects'] = self.get_scene_objects()['objects']
        else:
            for object in self.__main_group.to_dict()['objects']:
                scene['objects'].append(object)

        with open(self.__file_path, 'w') as file:
            json.dump(scene, file)

    def delete(self):
        os.remove(self.__file_path)

    @staticmethod
    def default_structure(name: str, order_load: int) -> dict[str, str | list]:
        scene = {
            "name": name,
            "order_load": order_load,
            "objects": []
        }

        return scene
