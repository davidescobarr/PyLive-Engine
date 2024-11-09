from enum import Enum
from typing import override

import pygame

from core.events.Event import Event
from core.properties.Image import Image
from core.utils.Convertors import hex_to_rgb
from core.utils.decorators.PropertyValue import VisibleValue


class TypesObject(Enum):
    Square = "Square"


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, x=0, y=0):
        self.x += x
        self.y += y
        return self


class Size:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class Object(pygame.sprite.Sprite, Image):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        Image.__init__(self)
        self.__size = Size(20, 20)
        self.__type = TypesObject.Square
        self.__color = (255, 255, 255)
        self.__position = Position(0, 0)
        self.__name = "object"
        self.__hex_color = "#FFFFFF"

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @VisibleValue(path="scale/", is_visible=True)
    def width(self) -> int:
        return self.__size.width

    @width.setter
    def width(self, value):
        if value >= 0:
            self.__size.width = value

    @VisibleValue(path="scale/", is_visible=True)
    def height(self) -> int:
        return self.__size.height

    @VisibleValue(path="position/", is_visible=True)
    def x(self) -> int:
        return self.__position.x

    @x.setter
    def x(self, value):
        if isinstance(value, int):
            self.__position.x = value

    @VisibleValue(path="position/", is_visible=True)
    def y(self) -> int:
        return self.__position.y

    @y.setter
    def y(self, value):
        if isinstance(value, int):
            self.__position.y = value

    @VisibleValue(path="color/", is_visible=True)
    def hex_color(self) -> str:
        return self.__hex_color

    @hex_color.setter
    def hex_color(self, value: str):
        if value.startswith("#") and len(value) == 7:
            self.__hex_color = value

    @height.setter
    def height(self, value):
        if value >= 0:
            self.__size.height = value

    def get_position(self) -> Position:
        return self.__position

    def get_type(self) -> TypesObject:
        return self.__type

    def get_color(self) -> tuple[int, int, int]:
        return hex_to_rgb(self.__hex_color)

    def get_size(self) -> Size:
        return self.__size

    @override
    def update(self, *args, **kwargs):
        pass

    def on_event(self, event: Event):
        pass

    def load_properties(self, properties):
        for path, prop_name, value in VisibleValue.find_visible_properties(self):
            keys = path.rstrip('/').split('/')
            d = properties
            for key in keys:
                d = d[key] if key in d else {}
            setattr(self, prop_name, d[prop_name] if prop_name in d else value)

    def save_properties(self) -> dict[str, any]:
        properties = VisibleValue.find_visible_properties(self)
        return VisibleValue.aggregate_properties(self, properties)

    def move(self, x: int, y: int):
        position = self.__position
        new_position = position.move(x, y)
        self.set_position(new_position)
