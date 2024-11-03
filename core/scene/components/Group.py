from typing import List, override

from core import Scene
from core.scene.SceneComponent import SceneComponent

class Group(SceneComponent):
    def __init__(self, scene: Scene, name: str, order: int):
        super().__init__("group", scene, order)
        self.__objects = []
        self.__name = name

    def add_object(self, scene_object: SceneComponent) -> None:
        new_objects = []
        if len(self.__objects) + 1 < scene_object.order or scene_object.order == -1:
            scene_object.order = len(self.__objects) + 1
        for i in range(len(self.__objects) + 2):
            if i == scene_object.order:
                new_objects.append(scene_object)
            if i < len(self.__objects):
                new_objects.append(self.__objects[i])

        self.__objects = new_objects

    def remove_object(self, order: int):
        if order < len(self.__objects):
            self.__objects.pop(order)
        else:
            print("Can't delete items which order not in range group items")

    def get_objects(self) -> List[SceneComponent]:
        return self.__objects

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @override
    def to_dict(self) -> {}:
        dict_objects = []

        for object in self.get_objects():
            dict_objects.append(object.to_dict())

        dict_group = {"name": self.__name, "type": self.type, "objects": dict_objects}

        return dict_group