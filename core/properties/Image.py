import pygame


class Image:
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