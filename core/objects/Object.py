from enum import Enum
from typing import override

import pygame

from core.events.Event import Event
from core.properties.Image import Image


class TypesObject(Enum):
    Square = ''

TypesObject = Enum('TypesObject', ['Square'])

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, x = 0, y = 0):
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
        self.__size = Size(0, 0)
        self.__type = TypesObject.Square
        self.__color = (255, 255, 255)
        self.__position = Position(0, 0)
        self.__name = "object"

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    def get_size(self) -> Size:
        return self.__size

    def set_size(self, width, height):
        self.__size = Size(width, height)

    def get_type(self) -> TypesObject:
        return self.__type

    def set_color(self, color: tuple[int, int, int]) -> None:
        self.__color = color

    def get_color(self) -> tuple[int, int, int]:
        return self.__color

    def get_position(self) -> Position:
        return self.__position

    def set_position(self, position: Position):
        self.__position = position

    @override
    def update(self, *args, **kwargs):
        pass

    def on_event(self, event: Event):
        pass

    def load_properties(self, properties):
        scale = properties['scale']
        position = properties['position']
        color = None
        if "color" in properties:
            color = properties['color']
        self.set_position(Position(position["x"], position["y"]))
        self.set_size(scale["width"], scale["height"])
        if not color is None:
            self.set_color((color["r"], color["g"], color["b"]))

        if "image" in properties and isinstance(self, Image):
            image = properties["image"]["path_file"]
            self.set_image(image)

    def move(self, x: int, y: int):
        position = self.__position
        new_position = position.move(x, y)
        self.set_position(new_position)