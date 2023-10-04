import numpy as np
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Tile:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.index = self.get_available_index()

    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            if len(value) == 1:
                return self.symbol == value
            else:
                return self.name == value
        elif isinstance(value, int):
            return self.index == value
        elif isinstance(value, Tile):
            return all(
                [
                    self.name == value.name,
                    self.index == value.index,
                    self.symbol == value.symbol,
                ]
            )
        return False

    @classmethod
    def get_available_index(cls) -> int:
        if not hasattr(cls, "next_index"):
            cls.next_index = 0
            return cls.next_index
        cls.next_index += 1
        return cls.next_index


@dataclass
class Tiles:
    EMPTY = Tile("empty", "E")
    UNKNOWN = Tile("unknown", "U")
    VILLAGE_1 = Tile("village1", "1")
    VILLAGE_2 = Tile("village2", "2")
    WOOD = Tile("wood", "W")
    IRON = Tile("iron", "I")
    WHEAT = Tile("wheat", "H")
    GOLD = Tile("gold", "G")
    ENERGY_POT = Tile("energy_pot", "P")
    AGENT_1 = Tile("agent1", "H")
    AGENT_2 = Tile("agent2", "V")

    @classmethod
    def get(cls, index: int):
        for value in cls.__dict__.values():
            if isinstance(value, Tile) and index == getattr(value, "index", -100):
                return value
        return cls.UNKNOWN

        if agents not in range(4, 11):
            raise ValueError("Number of agents must be between between 3 and 11.")

        if width < 100 or height < 100:
            raise ValueError("Minimum map size must be 100x100.")

        if (wood + iron + gold) >= 50:
            raise ValueError("Resource tiles must be below 50% of total tiles.")


class Map:
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix

    def get_tile(self, pos: Position) -> Tile:
        return Tiles.get(self.matrix[pos.x][pos.y])

    def set_tile(self, pos: Position, tile: Tile):
        self.matrix[pos.x][pos.y] = tile.index

