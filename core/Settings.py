import json

from core.Scene import Scene
from core.utils.delegates.PropertyValueDelegate import DelegateNotifier


class Settings:
    def __init__(self, path_file_settings: str, folder: str):
        self.__is_loaded = False
        self.__is_new = True
        self.__path = path_file_settings
        self.__folder = folder

        self.__nameProject = ""
        self.__version = ""
        self.__versionEngine = ""
        self.__requirements = ""
        self.__pathAssets = ""
        self.__pathScene = ""
        self.__pathScripts = ""
        self.__compiler = ""
        self.__fps = 0
        self.__width_window = 0
        self.__height_window = 0
        self.__current_scene = ""
        self.__settings = {}

        self.__notify_update_name_project = DelegateNotifier()

        if not self.load():
            self.set_default_values()
            self.save()
        else:
            self.__is_new = False

    def set_default_values(self):
        self.__nameProject = "project"
        self.__version = "1.0"
        self.__versionEngine = "alpha"
        self.__requirements = ""
        self.__pathAssets = "assets/"
        self.__pathScene = "scene/"
        self.__pathScripts = "scripts/"
        self.__compiler = "default"
        self.__fps = 60
        self.__width_window = 400
        self.__height_window = 400
        self.__current_scene = ""
        self.__is_loaded = True

    def save(self) -> bool:
        self.__settings = {
            'name_project': self.__nameProject,
            'version': self.__version,
            'version_engine': self.__versionEngine,
            'requirements': self.__requirements,
            'path_assets': self.__pathAssets,
            'path_scene': self.__pathScene,
            'path_scripts': self.__pathScripts,
            'compiler': self.__compiler,
            'fps': self.__fps,
            'width_window': self.__width_window,
            'height_window': self.__height_window,
            'current_scene': self.__current_scene
        }

        if self.__settings is None:
            return False

        with open(self.__path, "w") as file:
            json.dump(self.__settings, file, indent=4)
        return True

    def load(self) -> bool:
        settings = None
        try:
            with open(self.__path) as file:
                settings = json.load(file)
        except:
            print("failed to load settings")
            return False

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
        self.__current_scene = settings['current_scene']

        self.__settings = settings

        self.__is_loaded = True

        return True

    def subscribe_change_title(self, func: callable):
        self.__notify_update_name_project.subscribe(func)

    def set_name_project(self, name: str) -> None:
        self.__nameProject = name
        self.__settings['name_project'] = name
        self.save()
        self.__notify_update_name_project.notify()

    def set_version(self, version: str) -> None:
        self.__version = version
        self.__settings['version'] = version
        self.save()

    def set_version_engine(self, version_engine: str) -> None:
        self.__versionEngine = version_engine
        self.__settings['version_engine'] = version_engine
        self.save()

    def set_requirements(self, requirements: str) -> None:
        self.__requirements = requirements
        self.__settings['requirements'] = requirements
        self.save()

    def set_path_assets(self, path_assets: str) -> None:
        self.__pathAssets = path_assets
        self.__settings['path_assets'] = path_assets
        self.save()

    def set_path_scene(self, path_scene: str) -> None:
        self.__pathScene = path_scene
        self.__settings['path_scene'] = path_scene
        self.save()

    def set_path_scripts(self, path_scripts: str) -> None:
        self.__pathScripts = path_scripts
        self.__settings['path_scripts'] = path_scripts
        self.save()

    def set_compiler(self, compiler: str) -> None:
        self.__compiler = compiler
        self.__settings['compiler'] = compiler
        self.save()

    def set_fps(self, fps: int) -> None:
        self.__fps = fps
        self.__settings['fps'] = fps
        self.save()

    def set_width_window(self, width_window: int) -> None:
        self.__width_window = width_window
        self.__settings['width_window'] = width_window
        self.save()

    def set_height_window(self, height_window: str) -> None:
        self.__height_window = height_window
        self.__settings['height_window'] = height_window
        self.save()

    def set_current_scene(self, scene: Scene) -> None:
        self.__current_scene = scene.get_scene_file()
        self.__settings['current_scene'] = scene.get_scene_file()
        self.save()

    @property
    def is_loaded(self) -> bool:
        return self.__is_loaded

    @property
    def name_project(self) -> str:
        return self.__nameProject

    @property
    def version(self) -> str:
        return self.__version

    @property
    def version_engine(self) -> str:
        return self.__versionEngine

    @property
    def requirements(self) -> str:
        return self.__requirements

    @property
    def path_assets(self) -> str:
        return self.__pathAssets

    @property
    def path_scene(self) -> str:
        return self.__pathScene

    @property
    def path_scripts(self) -> str:
        return self.__pathScripts

    @property
    def compiler(self) -> str:
        return self.__compiler

    @property
    def fps(self) -> int:
        return self.__fps

    @property
    def width_window(self) -> int:
        return self.__width_window

    @property
    def height_window(self) -> int:
        return self.__height_window

    @property
    def current_scene(self) -> str:
        return self.__current_scene

    @property
    def is_new(self):
        return self.__is_new

    @property
    def folder(self):
        return self.__folder