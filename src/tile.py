import arcade
import arcade.color as colors
from arcade.shape_list import create_polygon
from arcade.types import Color

from src.types import Coords

from .constants import *
from .tiles import Tiles, TileType

tile_color_mapper: dict[int, Color] = {
    Tiles.EMPTY.index: colors.GREEN,
    Tiles.UNKNOWN.index: colors.BLACK,
    Tiles.VILLAGE_1.index: colors.PURPLE,
    Tiles.VILLAGE_2.index: colors.BRONZE,
    Tiles.WOOD.index: colors.BROWN,
    Tiles.IRON.index: colors.GRAY,
    Tiles.WHEAT.index: colors.WHEAT,
    Tiles.GOLD.index: colors.GOLD,
    Tiles.ENERGY_POT.index: colors.PEAR,
    Tiles.AGENT_1.index: colors.BLUE,
    Tiles.AGENT_2.index: colors.RED,
}


class Tile:
    width: float
    height: float

    def __init__(
        self,
        coords: Coords,
        tile_type: TileType,
    ):
        self.coords = coords
        self.symbol = tile_type.symbol
        self.color = tile_color_mapper[tile_type.index]
        self.data_coords = self._precompute_data_coords(coords.x, coords.y)
        self.vertices = self._precompute_vertices(*self.data_coords)
        self._shape = create_polygon(self.vertices, self.color)

    def set_tile_type(self, tile_type: TileType):
        self.symbol = tile_type.symbol
        self.color = tile_color_mapper[tile_type.index]

    @property
    def shape(self):
        return self._shape

    def render(self):
        arcade.draw_polygon_filled(self.vertices, self.color)

        arcade.draw_text(
            self.symbol,
            self.data_coords[0],
            self.data_coords[1],
            colors.BLACK,
            16,
            width=20,
            align="center",
            anchor_x="center",
        )

    def render_border(self, color: Color):
        arcade.draw_polygon_outline(self.vertices, color, 4)

    @classmethod
    def _precompute_data_coords(cls, x: int, y: int) -> tuple[int, int]:
        x = int(x * cls.width + WINDOW_PADDING + BOARD_PADDING + cls.width / 2)
        y = int(y * cls.height + WINDOW_PADDING + BOARD_PADDING + cls.height / 2)
        return x, y

    @classmethod
    def _precompute_vertices(cls, x: int, y: int) -> list[tuple[float, float]]:
        vertices = [
            (x - cls.width / 2, y - cls.height / 2),
            (x - cls.width / 2, y + cls.height / 2),
            (x + cls.width / 2, y + cls.height / 2),
            (x + cls.width / 2, y - cls.height / 2),
        ]
        return vertices
