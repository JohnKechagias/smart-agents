from dataclasses import dataclass

import toml


@dataclass
class GameConfig:
    agents: int
    energy_pots: int
    energy_pots_energy: int
    golds: int
    energy_pot_price: int
    map_price: int
    width: int
    height: int
    team1: dict
    team2: dict
    resources: dict


def load_config(filepath: str) -> GameConfig:
    with open(filepath, "r") as f:
        config = GameConfig(**toml.load(f))
        if config.agents not in range(1, 11):
            raise ValueError("Number of agents must be between between 1 and 11.")

        if config.width < 30 or config.height < 30:
            raise ValueError("Minimum map size must be 100x100.")

        return config
