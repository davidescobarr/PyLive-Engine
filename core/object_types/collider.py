import main
from core.logger import TypesLog


class Collider:
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height

    def set_size(self, width: int, height: int) -> None:
        if width > 0 and height > 0:
            self.__width = width
            self.__height = height
        else:
            main.game.logger.log("Неверно указан размер объекта", TypesLog.WARNING)