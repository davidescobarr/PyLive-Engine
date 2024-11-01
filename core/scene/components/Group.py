from typing import List, override

from core import Scene
from core.scene.SceneComponent import SceneComponent

class Group(SceneComponent):
    def __init__(self, scene: Scene, name: str):
        super().__init__("group", scene)
        self.__objects = []
        self.__name = name

    def add_object(self, scene_object: SceneComponent) -> None:
        self.__objects.append(scene_object)

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

        dict_group = {"name": self.name, "type": self.type, "objects": dict_objects}

        return dict_group