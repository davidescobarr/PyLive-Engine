from engine.core.Project import Project


class Engine:
    def __init__(self, project: Project):
        self.__project = project

    @property
    def project(self):
        return self.__project