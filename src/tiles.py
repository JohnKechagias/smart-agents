from dataclasses import dataclass


@dataclass
class TileType:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.index = self._get_available_index()

    def __repr__(self) -> str:
        return f"TileType(name={self.name}, symbol={self.symbol}, index={self.index})"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            if len(value) == 1:
                return self.symbol == value
            else:
                return self.name == value
        elif isinstance(value, int):
            return self.index == value
        elif isinstance(value, TileType):
            return all(
                [
                    self.name == value.name,
                    self.index == value.index,
                    self.symbol == value.symbol,
                ]
            )
        return False

    @classmethod
    def _get_available_index(cls) -> int:
        if not hasattr(cls, "next_index"):
            cls.next_index = 0
            return cls.next_index
        cls.next_index += 1
        return cls.next_index


@dataclass
class Tiles:
    EMPTY = TileType("empty", "E")
    UNKNOWN = TileType("unknown", "U")
    VILLAGE_1 = TileType("village1", "1")
    VILLAGE_2 = TileType("village2", "2")
    WOOD = TileType("wood", "W")
    IRON = TileType("iron", "I")
    WHEAT = TileType("wheat", "H")
    GOLD = TileType("gold", "G")
    ENERGY_POT = TileType("energy_pot", "P")
    AGENT_1 = TileType("agent1", "O")
    AGENT_2 = TileType("agent2", "V")

    @classmethod
    def get(cls, index: int):
        for value in cls.__dict__.values():
            if isinstance(value, TileType) and index == getattr(value, "index", -100):
                return value
        return cls.UNKNOWN
