from core import Scene


class SceneComponent:
    def __init__(self, type: str, scene: Scene):
        self.__type = type
        self.__scene = scene

    @property
    def scene(self) -> Scene:
        return self.__scene

    @property
    def type(self) -> str:
        return self.__type

    def to_dict(self) -> {}:
        pass