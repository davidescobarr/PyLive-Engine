# Import from lib
import sys
from typing import Optional

import pygame
import random

# Import from project
from .logger import Logger, TypesLog

class Game:
    def __init__(self,
                 width: Optional[int] = 360,
                 height: Optional[int] = 480,
                 fps: Optional[int] = 30,
                 logger: Optional[Logger] = Logger(),
                 title: Optional[str] = 'Game'
                 ) -> None:
        self.__width = width
        self.__height = height
        self.__fps = fps
        self.__logger = logger
        self.__title = title
        self.__run = False
        self.__clock = None
        self.__screen = None

    @property
    def logger(self):
        return self.__logger

    @property
    def fps(self):
        return self.__fps

    @fps.setter
    def fps(self, fps):
        if fps > 0:
            self.__fps = fps
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
        pygame.init()
        pygame.mixer.init()  # для звука
        pygame.display.set_caption(self.__title)
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__run = True
        self.game_loop()

    def stop(self):
        self.__run = False
        pygame.display.quit()
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()

    def game_loop(self):
        while self.__run:
            self.__clock.tick(self.__fps)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.stop()