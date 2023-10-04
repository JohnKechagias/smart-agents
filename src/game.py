from dataclasses import dataclass

import toml

from src.agent import ResourcePile, Team, Village
from src.constants import Position, Tiles
from src.map import GameMap


@dataclass
class GameConfig:
    agents: int
    energy_pots: int
    golds: int
    energy_pot_price: int
    map_price: int
    width: int
    height: int
    team1: dict
    team2: dict
    resources: dict


class Game:
    @classmethod
    def initialize(cls):
        team1_resources = ResourcePile(**cls.config.team1)
        team2_resources = ResourcePile(**cls.config.team2)

        village1_center = Position(
            (cls.config.width * 3) // 10,
            (cls.config.height * 3) // 10,
        )

        village2_center = Position(
            (cls.config.width * 7) // 10,
            (cls.config.height * 7) // 10,
        )

        village1 = Village(village1_center, Tiles.VILLAGE_1)
        village2 = Village(village2_center, Tiles.VILLAGE_2)

        team1 = Team(village1, team1_resources, cls.config.agents, Tiles.AGENT_1)
        team2 = Team(village2, team2_resources, cls.config.agents, Tiles.AGENT_2)

        cls.map = GameMap(
            cls.config.width,
            cls.config.height,
            cls.config.resources["wood"],
            cls.config.resources["wheat"],
            cls.config.resources["iron"],
            cls.config.golds,
            cls.config.energy_pots,
            team1,
            team2
        )
        
    @classmethod
    def load_config(cls):
        with open("config.toml", "r") as f:
            config = toml.load(f)
            cls.config = GameConfig(**config)
