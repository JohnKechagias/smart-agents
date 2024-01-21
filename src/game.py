from .agent import ResourcePile, Team, Village
from .config import GameConfig, load_config
from .game_map import GameMap
from .tiles import Tiles
from .types import Coords


class Game:
    config: GameConfig

    @classmethod
    def initialize(cls, filepath: str):
        config = load_config(filepath)
        team1_resources = ResourcePile(**config.team1)
        team2_resources = ResourcePile(**config.team2)

        village1_center = Coords(
            (config.width * 3) // 10,
            (config.height * 3) // 10,
        )

        village2_center = Coords(
            (config.width * 7) // 10,
            (config.height * 7) // 10,
        )

        print(f"Center of village 1: {village1_center}")
        print(f"Center of village 2: {village2_center}")

        village1 = Village(village1_center, Tiles.VILLAGE_1)
        village2 = Village(village2_center, Tiles.VILLAGE_2)

        cls.map = GameMap(
            config.width,
            config.height,
            config.resources["wood"],
            config.resources["wheat"],
            config.resources["iron"],
            config.golds,
            config.energy_pots,
            [village1, village2],
            config.agents,
        )

        team1 = Team(village1, team1_resources, Tiles.AGENT_1, config)
        team2 = Team(village2, team2_resources, Tiles.AGENT_2, config)
        cls.teams = [team1, team2]

        for team in cls.teams:
            cls.map.generate_players(team, config.agents)

        cls.map.print_map()

    @classmethod
    def run(cls):
        stop = False
        while not stop:
            for team in cls.teams:
                for agent in team.agents:
                    agent.update()
                    agent.print_map()

                team.print_resources()

            for team in cls.teams:
                if not team.resources.wanted_resources:
                    print(f"Team {team.id} Won!")
                    team.print_resources()
                    stop = True
                    break
