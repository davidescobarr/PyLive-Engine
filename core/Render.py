import pygame.display

from core.objects.Object import TypesObject
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
            position = object.get_position()
            size = object.get_size()

            if isinstance(object, Image):
                if object.is_use_image():
                    object_surface = pygame.transform.scale(object.get_image(), (size.width, size.height))
                    self.__sc.blit(object_surface, object_surface.get_rect(center=(position.x, position.y)))
                    continue

            match object.get_type().name:
                case TypesObject.Square.name:
                    pygame.draw.rect(self.__sc, object.get_color(), (position.x - size.width/2, position.y - size.height/2, size.width, size.height))

        if not self.__scene.dev:
            pygame.display.flip()
            pygame.display.update()

    def get_surface(self):
        return self.__sc