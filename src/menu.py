import arcade
from arcade.shape_list import Shape, create_rectangle_outline
from arcade.types import Color

from .constants import MENU_WIDTH, Point


class Menu:
    def __init__(self, point: Point, color: Color, width: int, height: int):
        self.point = point
        self.color = color
        self.width = width
        self.height = height
        self.label_font_size = 18
        self.label_width = 200
        self.text_objects: list[arcade.Text] = []

        self.team1_resourses_text = arcade.Text(
            text="",
            x=int(self.point[0] - 0.47 * MENU_WIDTH),
            y=int(self.point[1]),
            color=self.color,
            font_size=self.label_font_size,
            width=self.label_width,
            anchor_x="left",
        )

        self.round_text = arcade.Text(
            text="",
            x=int(self.point[0] - 0.05 * MENU_WIDTH),
            y=int(self.point[1]),
            color=self.color,
            font_size=self.label_font_size,
            width=self.label_width,
        )

        self.team2_resourses_text = arcade.Text(
            text="",
            x=int(self.point[0] + 0.1 * MENU_WIDTH),
            y=int(self.point[1]),
            color=self.color,
            font_size=self.label_font_size,
            width=self.label_width,
        )

    @property
    def shape(self) -> Shape:
        return create_rectangle_outline(
            *self.point, self.width, self.height, self.color, 1
        )

    def render(self, team1_resourses: str, team2_resourses: str, round: int):
        self.team1_resourses_text.text = team1_resourses
        self.round_text.text = f"Round {round}"
        self.team2_resourses_text.text = team2_resourses
        self.team1_resourses_text.draw()
        self.round_text.draw()
        self.team2_resourses_text.draw()
