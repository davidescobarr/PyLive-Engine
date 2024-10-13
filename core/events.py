class Event:
    def __init__(self, type: int):
        self.__cancel = False
        self.__type = type

    def set_cancelled(self, cancel: bool) -> None:
        self.__cancel = cancel

    @property
    def type(self) -> int:
        return self.__type