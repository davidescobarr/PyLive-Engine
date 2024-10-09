import pygame
from pygame import SurfaceType

import main
from core.logger import TypesLog
from core.properties.property import ObjectProperty


class Object:
    def __init__(self, name: str):
        self.__name = name
        self.__id = 0
        self.__list_of_properties = []

    def add_property(self, object_property: ObjectProperty) -> None:
        self.__list_of_properties.append(object_property)

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        if id > 0:
            self.__id = id
        else:
            main.game.logger.log("Невозможно установить отрицательный id", TypesLog.WARNING)

    def before_update(self) -> None: ...

    def update_properties(self):
        for object_property in self.__list_of_properties:
            object_property.update(self)

    def update(self) -> None: ...

    def after_update(self) -> None: ...