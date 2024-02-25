import numpy as np

from .tiles import Tiles, TileType
from .types import Coords


class Map:
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.height, self.width = self.matrix.shape
        self.size = self.height * self.width
        self.positions = [
            Coords(x, y) for x in range(self.height) for y in range(self.width)
        ]

    def get_tile(self, pos: Coords) -> TileType:
        if not self.is_pos_valid(pos):
            return Tiles.INVALID

        return Tiles.get(self.matrix[pos.x][pos.y])

    def set_tile(self, pos: Coords, tile: TileType):
        self.matrix[pos.x][pos.y] = tile.index

    def print(self, filename: str):
        with open(filename, "w") as f:
            for i in range(self.width):
                for j in range(self.height):
                    symbol = Tiles.get(self.matrix[j][i]).symbol
                    f.write(symbol)

                f.write("\n")

    def is_pos_valid(self, coords: Coords) -> bool:
        x = coords.x
        y = coords.y
        return 0 <= x <= self.matrix.shape[0] and 0 <= y <= self.matrix.shape[1]
