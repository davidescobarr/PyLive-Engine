from typing import override

import pygame

from core.properties.Properties import Properties


class Image(Properties):
    def __init__(self):
        self.__use_image = False
        self.__image = None
        self.__path_image = ""

    def set_image(self, path_image: str) -> None:
        self.__image = pygame.image.load(path_image)
        if not self.__image is None:
            self.__path_image = path_image
            self.__use_image = True

    def get_image(self):
        return self.__image

    def is_use_image(self) -> bool:
        return self.__use_image

    def get_path_image(self) -> str:
        return self.__path_image

    @override
    def have_alternative_render(self) -> bool:
        return True

    @override
    def alternative_render(self, surface: pygame.Surface, object):
        if self.__use_image:
            object_surface = pygame.transform.scale(self.get_image(), (object.get_size().width, object.get_size().height))
            surface.blit(object_surface, object_surface.get_rect(center=(object.get_position().x, object.get_position().y)))