from dataclasses import dataclass


@dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
