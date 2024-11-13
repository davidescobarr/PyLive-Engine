import json


class GlobalSettings:
    def __init__(self):
        self.__last_project_file = ""
        self.__current_lang = ""
        self.__path_to_file = ""
        self.load("./settings.json")

    def load(self, path_to_file: str):
        with open(path_to_file, "r") as file:
            data = json.load(file)
            self.__path_to_file = path_to_file
            self.__last_project_file = data["last_project_path"]
            self.__current_lang = data["current_language"]

    def save(self):
        if self.__path_to_file != "":
            with open(self.__path_to_file, "w") as file:
                data = {
                    "last_project_path": self.__last_project_file,
                    "current_language": self.__current_lang
                }
                json.dump(data, file, indent=4)

    @property
    def lang(self):
        return self.__current_lang

    @lang.setter
    def lang(self, value: str):
        self.__current_lang = value

    @property
    def last_project_file(self):
        return self.__last_project_file

global_settings = GlobalSettings()