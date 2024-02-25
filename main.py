from src.config import load_config
from src.constants import *
from src.game import Game
from src.get_configuration import ConfigMenu


def main():
    config_menu = ConfigMenu()
    config_menu.show()
    config_path = config_menu.config_path
    print(f"config file: {config_path}")
    config = load_config(config_path)
    game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE, config)
    game.run()


if __name__ == "__main__":
    main()
