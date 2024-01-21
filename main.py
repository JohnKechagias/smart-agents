from src.game import Game


def main():
    Game.initialize("config.toml")
    Game.run()

if __name__ == "__main__":
    main()
