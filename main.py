from src.config import load_config
from src.constants import *
from src.game import Game
from src.get_configuration import GetConfiguration


def main():
    configpath = GetConfiguration.show()
    print("config file: " + configpath)

    config = load_config(configpath)
    game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE, config)
    game.run()



if __name__ == "__main__":
    main()
