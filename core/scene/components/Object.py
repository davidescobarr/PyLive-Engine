import sys
from typing import override
from xmlrpc.client import boolean

from core import Scene
from core.objects.Object import Object, Size
from core.scene.SceneComponent import SceneComponent
from core.utils.decorators.PropertyValue import VisibleValue


class SceneObject(SceneComponent):
    def __init__(self, scene: Scene, object: Object, order: int):
        super().__init__("object", scene, order)
        self.__object = object

    @VisibleValue
    def width(self) -> int:
        return self.__object.get_size().width

    @width.setter
    def width(self, width: int):
        self.__object.set_size(width, self.__object.get_size().height)

    @VisibleValue
    def height(self) -> int:
        return self.__object.get_size().height

    @height.setter
    def height(self, height: int):
        self.__object.set_size(self.__object.get_size().width, height)

    def set_size(self, size: Size) -> None:
        self.__object.set_size(size.width, size.height)

    def get_size(self) -> Size:
        return self.__object.get_size()

    def set_new_class(self, new_class: Object.__class__) -> None:
        self.__object = new_class()

    @VisibleValue
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
            "properties": {
                "class": sys.modules[self.__object.__class__.__module__].__file__,
                "className": self.__object.__class__.__name__,
                "position": {
                    "x": self.__object.get_position().x,
                    "y": self.__object.get_position().y
                },
                "scale": {
                    "width": self.__object.get_size().width,
                    "height": self.__object.get_size().height
                },
                "color": {
                    "r": self.__object.get_color()[0],
                    "g": self.__object.get_color()[1],
                    "b": self.__object.get_color()[2]
                }
            }
        }

        if self.__object.is_use_image():
            dict_object["properties"]["image"] = {"path_file": self.__object.get_path_image()}

        return dict_object