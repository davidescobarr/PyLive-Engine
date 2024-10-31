class Project:
    def __init__(self, path_project):
        if path_project == '':
            raise Exception("Null project")

        self.__scene = None
        self.__objects = []
        self.__path_project = path_project

    def load_scene(self):
        pass

    @property
    def path_project(self):
        return self.__path_project