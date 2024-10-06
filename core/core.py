# Import from lib
from msilib.schema import Property
from typing import Optional

import pygame
import random

# Import from project
import logger
from core.logger import Logger, TypesLog


class Game:
    def __init__(self,
                 width: Optional[int] = 360,
                 height: Optional[int] = 480,
                 fps: Optional[int] = 30,
                 logger: Optional[Logger] = Logger(),
                 name: Optional[str] = 'Game'
                 ) -> None:
        self.__width = width
        self.__height = height
        self.__fps = fps
        self.__logger = logger
        self.__name = name

    @property
    def fps(self):
        return self.__FPS

    @fps.setter
    def fps(self, fps):
        if fps > 0:
            self.__FPS = fps
        else:
            self.__logger.log("Невозможно установить отрицательный FPS", TypesLog.WARNING)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def set_size(self, width: int, height: int):
        if width > 0 and height > 0:
            self.__width = width
            self.__height = height
        else:
            self.__logger.log("Невозможно установить разрешение " + width + "x" + height, TypesLog.WARNING)

    def start(self):
        # создаем игру и окно
        pygame.init()
        pygame.mixer.init()  # для звука
        screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption(self.__name)
        clock = pygame.time.Clock()