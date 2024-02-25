from enum import IntEnum

from arcade import color as colors

Point = tuple[float, float]


class Theme(IntEnum):
    LIGHT = 0
    DARK = 1


# Color theme of the program
COLOR_THEME = Theme.DARK
# Title of the window
TITLE = "Smart Agents"


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1200
WINDOW_PADDING = 10
BOARD_PADDING = 0

MENU_HEIGHT = 80
MENU_WIDTH = WINDOW_WIDTH - 2 * WINDOW_PADDING
MENU_PADDING = 10

WIDTH = 100
TILE_WIDTH = (WINDOW_WIDTH - 2 * WINDOW_PADDING) / WIDTH
TILE_HEIGHT = TILE_WIDTH
