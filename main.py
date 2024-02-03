from src.config import load_config
from src.constants import *
from src.game import Game


def main():
    configpath = "config.toml"
    config = load_config(configpath)
    game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE, config)
    game.run()


if __name__ == "__main__":
    main()
