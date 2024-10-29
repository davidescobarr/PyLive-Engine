import json

class Settings:
    def __init__(self, path_file_settings: str):
        with open(path_file_settings) as file:
            settings = json.load(file)

        if settings is None:
            print("failed to load settings")
            return

        self.__nameProject = settings['name_project']
        self.__version = settings['version']
        self.__versionEngine = settings['version_engine']
        self.__requirements = settings['requirements']
        self.__pathAssets = settings['path_assets']
        self.__pathScene = settings['path_scene']
        self.__pathScripts = settings['path_scripts']
        self.__compiler = settings['compiler']
        self.__fps = settings['fps']
        self.__width_window = settings['width_window']
        self.__height_window = settings['height_window']

    @property
    def name_project(self):
        return self.__nameProject

    @property
    def version(self):
        return self.__version

    @property
    def version_engine(self):
        return self.__versionEngine

    @property
    def requirements(self):
        return self.__requirements

    @property
    def path_assets(self):
        return self.__pathAssets

    @property
    def path_scene(self):
        return self.__pathScene

    @property
    def path_scripts(self):
        return self.__pathScripts

    @property
    def compiler(self):
        return self.__compiler

    @property
    def fps(self):
        return self.__fps

    @property
    def width_window(self):
        return self.__width_window

    @property
    def height_window(self):
        return self.__height_window