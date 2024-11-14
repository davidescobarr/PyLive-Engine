from typing import override

from core.events.Event import Event
from core.objects.Object import Object, Position
from core.utils.decorators.PropertyValue import VisibleValue


class CustomObject(Object):
    def __init__(self):
        super().__init__()
        self.__hui_sosal = False

    @override
    def on_event(self, event: Event):
        pass

    @override
    def update(self, *args, **kwargs):
        self.move(1, 1)

    @VisibleValue(is_visible=True)
    def hui_sosal(self) -> bool:
        return self.__hui_sosal

    @hui_sosal.setter
    def hui_sosal(self, value: bool):
        self.__hui_sosal = value