import pygame
from pygame import SurfaceType

import main
from core.logger import TypesLog


class Object(pygame.sprite.Sprite):
    def __init__(self, name: str, width: int, height: int):
        pygame.sprite.Sprite.__init__(self)
        self.__width = width
        self.__height = height
        self.__name = name
        self.__image = pygame.Surface((self.__width, height))
        self.__id = 0

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

    def update(self) -> None: ...

    def after_update(self) -> None: ...

    def set_size(self, width: int, height: int) -> None:
        if width > 0 and height > 0:
            self.__width = width
            self.__height = height
        else:
            main.game.logger.log("Неверно указан размер объекта", TypesLog.WARNING)

    @property
    def image(self) -> SurfaceType:
        return self.__image

    @image.setter
    def image(self, image: SurfaceType) -> None:
        self.__image = image