import json

class GlobalSettings:
    def __init__(self):
        self.__last_project_file = ""
        self.__current_lang = ""
        self.__path_to_file = ""
        if not self.load("./settings.json"):
            self.__current_lang = "ru"
            self.save()

    def load(self, path_to_file: str):
        try:
            with open(path_to_file, "r") as file:
                data = json.load(file)
                self.__path_to_file = path_to_file
                self.__current_lang = data["current_language"]
                return True
        except:
            pass

        return False

    def save(self):
        if self.__path_to_file != "":
            with open(self.__path_to_file, "w") as file:
                data = {
                    "current_language": self.__current_lang
                }
                json.dump(data, file, indent=4)

    @property
    def lang(self):
        return self.__current_lang

    @lang.setter
    def lang(self, value: str):
        self.__current_lang = value

global_settings = GlobalSettings()