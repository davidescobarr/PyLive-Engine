from core import Scene


class SceneComponent:
    def __init__(self, type: str, scene: Scene, order: int):
        self.__type = type
        self.__scene = scene
        self.__order = order

    @property
    def order(self) -> int:
        return self.__order

    @order.setter
    def order(self, order: int):
        if order >= 0:
            self.__order = order
        else:
            self.__order = -1

    @property
    def name(self):
        return ""

    @name.setter
    def name(self, name: str):
        pass

    @property
    def scene(self) -> Scene:
        return self.__scene

    @property
    def type(self) -> str:
        return self.__type

    def to_dict(self) -> {}:
        pass