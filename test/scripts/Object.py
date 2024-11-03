from typing import override

from core.events.Event import Event
from core.objects.Object import Object, Position


class CustomObject(Object):
    def __init__(self):
        super().__init__()

    @override
    def on_event(self, event: Event):
        pass

    @override
    def update(self, *args, **kwargs):
        self.move(1, 1)