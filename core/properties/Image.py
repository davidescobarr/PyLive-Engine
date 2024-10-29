import pygame


class Image:
    def __init__(self):
        self.__use_image = False
        self.__image = None

    def set_image(self, path_image: str):
        self.__image = pygame.image.load(path_image)
        if not self.__image is None:
            self.__use_image = True

    def get_image(self):
        return self.__image

    def is_use_image(self):
        return self.__use_image