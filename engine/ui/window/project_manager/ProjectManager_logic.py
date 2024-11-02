import json

from PySide6.scripts.pyside_tool import project


class LastProject:
    def __init__(self, name, path, version, last_open):
        self.__name = name
        self.__path = path
        self.__version = version
        self.__last_open = last_open

    @property
    def name(self) -> str:
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def engine_version(self) -> str:
        return self.__version

    @property
    def last_open(self) -> str:
        return self.__last_open

    @last_open.setter
    def last_open(self, date: str) -> None:
        self.__last_open = date

def get_settings() -> str:
    return "./engine/settings/last_projects.json"

class Projects:
    def __init__(self):
        self.__projects = []
        self.init_projects()

    def get_save_file(self) -> str:
        return "./engine/settings/last_projects.json"

    def init_projects(self):
        with open(get_settings()) as file:
            settings = json.load(file)

        json_projects = settings['projects']
        projects = []

        for json_project in json_projects:
            project = LastProject(json_project['name'], json_project['path'], json_project['version_engine'],
                                  json_project['last_open'])
            projects.append(project)

        self.__projects = projects

    def add_new_project(self, project: LastProject):
        self.__projects.append(project)
        self.save()

    def remove_project(self, project: LastProject):
        self.__projects.remove(project)
        self.save()

    def get_last_projects(self):
        return self.__projects

    def get_formatted_last_projects(self):
        formatted_projects = []

        for project in self.__projects:
            formatted_projects.append({
                "name": project.name,
                "path": project.path,
                "version": project.engine_version,
                "last_open": project.last_open
            })

        return formatted_projects

    def save(self):
        objects = []

        for project in self.__projects:
            objects.append({
                "name": project.name,
                "path": project.path,
                "version_engine": project.engine_version,
                "last_open": project.last_open
            })

        save_dict = {
            "projects": objects
        }

        with open(self.get_save_file(), "w") as file:
            json.dump(save_dict, file)