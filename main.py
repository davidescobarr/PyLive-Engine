from core.core import Game
from core.settings import Settings

if __name__ == '__main__':
    game = Game(Settings("./example_project/settings.json"))
    game.start()