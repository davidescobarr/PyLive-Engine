from core.core import Game
from core.logger import Logger, TypesLog

game = Game(360, 480, 60, Logger(), "my game")

if __name__ == '__main__':
    game.set_size(1280, 720)
    game.start()