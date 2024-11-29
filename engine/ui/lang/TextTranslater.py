import os
from enum import Enum
from glob import glob
from engine.core.GlobalSettings import global_settings

class Languages(Enum):
    Russian = "ru"
    English = "en"
    Belarusian = "by"

languages = {
            "Русский": Languages.Russian,
            "English": Languages.English,
            "Беларускі": Languages.Belarusian
        }

class TextTranslater:
    def __init__(self, lang_path: str, language: Languages = Languages.English):
        self.__language = language
        self.__lang_keys = {}
        self.__lang_path = lang_path
        self.__lang_file = lang_path + "/" + language.value + ".lang"
        self.init_language()

    def init_language(self):
        try:
            with open(self.__lang_file, 'r', encoding='utf-8') as f:
                self.__lang_keys = {}
                lang_file = f.read()
                lang_file = lang_file.split("\n")
                for line in lang_file:
                    if line.startswith("#"):
                        continue
                    line = line.split("=")
                    self.__lang_keys[line[0]] = line[1]
        except FileNotFoundError:
            print("Language file not found")
            return

    def get_translate(self, lang_key: str):
        if not self.__lang_keys.get(lang_key) is None:
            return self.__lang_keys.get(lang_key)

        return lang_key

    def switch_language(self, language: Languages):
        self.__language = language
        self.__lang_file = self.__lang_path + "/" + language.value + ".lang"
        self.init_language()
        global_settings.lang = language.value
        global_settings.save()

    def get_languages(self):
        current_language = self.get_current_language()
        # Отображаем текущий язык первым
        sorted_languages = {k: v for k, v in sorted(languages.items(), key=lambda item: item[1] != current_language)}
        return sorted_languages

    def get_current_language(self):
        return self.__language

    @staticmethod
    def get_language_by_code(code: str):
        for lang in Languages:
            if lang.value == code:
                return lang
        return None

    @staticmethod
    def get_files(directory):
        """Get a list of JSON files in the specified directory."""
        return glob(os.path.join(directory, '*.lang'))

text_translator = TextTranslater("engine/ui/lang")
lang = TextTranslater.get_language_by_code(global_settings.lang)
if lang is not None:
    text_translator.switch_language(lang)