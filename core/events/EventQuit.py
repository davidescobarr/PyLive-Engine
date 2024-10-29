from core.events.Event import Event


class EventQuit(Event):
    def __init__(self):
        super().__init__()