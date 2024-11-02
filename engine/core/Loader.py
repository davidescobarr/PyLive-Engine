import os
from typing import Optional

from PySide6.QtWidgets import QMainWindow

from core.Settings import Settings
from engine.core.Project import Project

class Loader:
    def __init__(self, MainWindow: QMainWindow):
        self.__path = ""
        self.__settings = ""
        self.MainWindow = MainWindow

    def load_engine(self, path_project: str) -> bool:
        print("Load engine...")
        self.__path = path_project
        project = self.open_project(path_project)

        if project is None:
            print(f"Project not loaded at path {path_project}")
            return False

        project.init_scenes()

        if len(project.get_scenes()) < 1:
            print("No one scene not found...")
            print("Create new scene...")
            project.create_new_scene("scene")

            project.init_scenes()

            if len(project.get_scenes()) < 1:
                print("Engine can't create new correctly scene...")
                return False

        project.init_current_scene(project.get_scenes()[0])

        # load engine window

        return True

    def create_project(self, folder: str, name_project: str) -> Project:
        settings = Settings(folder + "/settings.json")

        if not settings.is_new:
            return self.open_project(folder)

        settings.set_default_values()
        settings.set_name_project(name_project)
        settings.save()

        os.makedirs(os.path.join(folder, 'assets'), exist_ok=True)
        os.makedirs(os.path.join(folder, 'scripts'), exist_ok=True)
        os.makedirs(os.path.join(folder, 'scene'), exist_ok=True)

        return self.open_project(folder)

    @staticmethod
    def open_project(folder) -> Optional[None | Project]:
        settings = Settings(folder + "/settings.json")

        if settings.is_loaded:
            return Project(folder, settings)

        return None