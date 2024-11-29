from core.Core import Game
from core.Settings import Settings

class StartGame:
    def __init__(self):
        pass

    def start(self):
        print("Settings load...")
        settings = Settings(self.get_resource_path("files/settings.json"), self.get_resource_path("files"))
        print("Settings loaded")
        print("Load core...")
        game = Game(settings)
        print("Core loaded")
        print("Start game...")
        game.run()

    @staticmethod
    def get_resource_path(relative_path):
        """Возвращает полный путь к файлам в скомпилированном с помощью PyInstaller приложении."""
        # Если мы работаем в скомпилированном приложении
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        # Если скрипт запущен в интерпретаторе
        else:
            return os.path.join(os.path.abspath('.'), relative_path)

if __name__ == "__main__":
    StartGame().start()