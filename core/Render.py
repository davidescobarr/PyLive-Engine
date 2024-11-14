import pygame.display

from core.properties.Image import Image
from core.Scene import Scene


class Render:
    def __init__(self, scene: Scene, width_window: int, height_window: int):
        self.__scene = scene
        if scene.dev:
            self.__sc = pygame.Surface((1920, 1080))
        else:
            self.__sc = pygame.display.set_mode((width_window, height_window))

    def update(self):
        self.__sc.fill((0, 0, 0))

        for object in self.__scene.get_objects():
            object.get_render(self.__sc)

        if not self.__scene.dev:
            pygame.display.flip()
            pygame.display.update()

    def get_surface(self):
        return self.__sc