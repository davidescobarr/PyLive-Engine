from PyQt6.QtWidgets import QWidget

from engine.core.Project import Project


class Engine(QWidget):
    def __init__(self, project: Project):
        super().__init__()

        self.__project = project

    def init_ui(self):
        pass