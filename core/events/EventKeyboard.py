import pygame
from pygame.event import EventType

from core.events.Event import Event


class EventKeyboard(Event):
    def __init__(self, event):
        super().__init__()
        self.__event = event

    @property
    def event(self):
        return self.__event