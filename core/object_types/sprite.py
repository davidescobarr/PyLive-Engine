import pygame
from pygame import SurfaceType

import main
from core.logger import TypesLog


class Sprite(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        pygame.sprite.Sprite.__init__(self)
        self.__width = width
        self.__height = height
        self.__image = pygame.Surface((self.__width, height))

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