from typing import Optional

import main
from core.logger import TypesLog
from core.object import Object


class Scene:
    def __init__(self, name: str):
        self.__name = name
        self.__objects = []

    def add_object(self, game_object: Object) -> None:
        game_object.id = self.__objects.__sizeof__() - 1
        self.__objects.append(game_object)

    def get_object(self, id: int) -> Optional[Object, None]:
        for game_object in self.__objects:
            if game_object.id == id:
                return game_object

        return None

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        if name != '':
            self.__name = name
        else:
            main.game.logger.log("Невозможно установить пустое имя для сцены", TypesLog.WARNING)

    def update(self) -> None:
        for game_object in self.__objects:
            game_object.before_update()
            game_object.update()
            game_object.after_update()