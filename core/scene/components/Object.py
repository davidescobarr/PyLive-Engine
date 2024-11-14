import sys
from typing import override

from core import Scene
from core.objects.Object import Object, Size
from core.scene.SceneComponent import SceneComponent


class SceneObject(SceneComponent):
    def __init__(self, scene: Scene, object: Object, order: int):
        super().__init__("object", scene, order)
        self.__object = object

    @property
    def object(self) -> Object:
        return self.__object

    @property
    def width(self) -> int:
        return self.__object.get_size().width

    @width.setter
    def width(self, width: int):
        self.set_size(width, self.__object.get_size().height)

    @property
    def height(self) -> int:
        return self.__object.get_size().height

    @height.setter
    def height(self, height: int):
        self.set_size(self.__object.get_size().width, height)

    def set_size(self, size: Size) -> None:
        self.__object.width = size.width
        self.__object.height = size.height

    def set_size(self, width: int, height: int) -> None:
        self.__object.width = width
        self.__object.height = height

    def get_size(self) -> Size:
        return self.__object.get_size()

    def set_new_class(self, new_class: Object.__class__) -> None:
        self.__object = new_class()

    @property
    def name(self) -> str:
        return self.__object.name

    @name.setter
    def name(self, name: str):
        self.__object.name = name

    @override
    def to_dict(self) -> {}:
        dict_object = {
            "name": self.name,
            "type": self.type,
            "properties": self.__object.save_properties()
        }

        dict_object["properties"]["class"] = sys.modules[self.__object.__class__.__module__].__file__
        dict_object["properties"]["className"] = self.__object.__class__.__name__

        return dict_object