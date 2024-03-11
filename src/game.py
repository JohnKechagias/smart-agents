from itertools import product
from typing import Literal

import arcade

from .agent import ResourcePile, Team, Village
from .config import GameConfig
from .constants import MENU_HEIGHT, MENU_PADDING, WINDOW_PADDING, colors
from .game_map import GameMap
from .logger import LOGGER
from .menu import Menu
from .tile import Tile
from .tiles import Tiles
from .types import Coords


class Game(arcade.Window):
    def __init__(
        self,
        width: int,
        height: int,
        title: str,
        game_config: GameConfig,
    ):
        super().__init__(
            width=width,
            height=height + MENU_HEIGHT,
            title=title,
            samples=16,
        )
        Tile.height = (height - 2 * WINDOW_PADDING) / game_config.height
        Tile.width = Tile.height

        self.is_paused = False
        self.game_config = game_config

        menu_center = (
            width / 2,
            height + MENU_HEIGHT - MENU_PADDING - MENU_HEIGHT / 2,
        )
        self.menu = Menu(menu_center, colors.WHITE_SMOKE, width, MENU_HEIGHT)
        self.background_color = colors.LICORICE

        self.initialize(game_config)
        self.setup(game_config.width)

    def reset(self):
        self.initialize(self.game_config)
        self.setup(self.game_config.width)

    def setup(self, size: int):
        self.round = 1
        # A list with all the default tile shapes and the menu shape. Its
        # used to speed up the rendering of board in its default state,
        # meaning when all the tiles are owned by nature. So when a tile
        # is owned by nature, we don't have to explicitly render it by
        # adding it to the tiles_to_render list.
        self.shapes_list = arcade.shape_list.ShapeElementList()

        # A list with all the valid tile coordinates, meaning from (0, 0),
        # (0, 1) ... (BOARD_SIZE, BOARD_SIZE)
        tile_coords = [Coords(*i) for i in product(range(size), repeat=2)]
        # A list that countains all of the tile instances. In this case, hexagons.
        self.tiles = [Tile(i, Tiles.EMPTY) for i in tile_coords]

        # Populate the shape list with the default tile shapes.
        for tile in self.tiles:
            self.shapes_list.append(tile.shape)

    def initialize(self, config: GameConfig):
        LOGGER.info(f"Creating resource piles...")
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

        LOGGER.info(f"Center of village 1: {village1_center}")
        LOGGER.info(f"Center of village 2: {village2_center}")

        LOGGER.info(f"Creating villages...")
        village1 = Village(village1_center, Tiles.VILLAGE_1)
        village2 = Village(village2_center, Tiles.VILLAGE_2)

        LOGGER.info(f"Creating map...")
        self.map = GameMap(
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
        self.map_to_show = self.map.matrix
        self.selected_team: Literal[0, 1] = 0
        self.selected_agent_num = 0

        LOGGER.info(f"Creating teams...")
        team1 = Team(village1, team1_resources, Tiles.AGENT_1, config)
        team2 = Team(village2, team2_resources, Tiles.AGENT_2, config)
        self.teams = [team1, team2]

        LOGGER.info(f"Creating agents...")
        for team in self.teams:
            self.map.generate_players(team, config.agents, config.map_price)

        self.map.print_map()

    def on_update(self, delta_time: float):
        if self.is_paused:
            return

        for team in self.teams:
            for agent in team.agents:
                agent.update()

        for team in self.teams:
            if not team.resources.wanted_resources:
                LOGGER.info(f"Team {team.id} Won!")
                exit()

    def on_draw(self):
        for tile, tile_index in zip(self.tiles, self.map_to_show.flat):
            tile.set_tile_type(Tiles.get(tile_index))

        self.clear()
        self.shapes_list.draw()

        for tile in self.tiles:
            tile.render()

        self.menu.render(
            self.teams[0].resources.get_resourse_repr(),
            self.teams[1].resources.get_resourse_repr(),
            self.round,
        )

    def on_key_press(self, symbol: int, modifiers: int):
        numbers_mapper = {
            arcade.key.KEY_0: 9,
            arcade.key.KEY_1: 0,
            arcade.key.KEY_2: 1,
            arcade.key.KEY_3: 2,
            arcade.key.KEY_4: 3,
            arcade.key.KEY_5: 4,
            arcade.key.KEY_6: 5,
            arcade.key.KEY_7: 6,
            arcade.key.KEY_8: 7,
            arcade.key.KEY_9: 8,
        }

        match symbol:
            case arcade.key.P:
                self.pause()
            case arcade.key.S:
                self.resume()
            case arcade.key.R:
                self.restart()
            case symbol if symbol in numbers_mapper.keys():
                selected_agent_num = numbers_mapper[symbol]
                if selected_agent_num >= self.game_config.agents:
                    return

                self.selected_agent_num = selected_agent_num
                agent = self.teams[self.selected_team].agents[self.selected_agent_num]
                self.map_to_show = agent.map.matrix
            case arcade.key.ENTER:
                self.map_to_show = self.map.matrix
            case arcade.key.MINUS:
                self.selected_team = 0
                agent = self.teams[self.selected_team].agents[self.selected_agent_num]
                self.map_to_show = agent.map.matrix
            case arcade.key.EQUAL:
                self.selected_team = 1
                agent = self.teams[self.selected_team].agents[self.selected_agent_num]
                self.map_to_show = agent.map.matrix

    def pause(self):
        LOGGER.info("GAME PAUSED")
        self.is_paused = True

    def resume(self):
        LOGGER.info("GAME RESUMED")
        self.is_paused = False

    def restart(self):
        LOGGER.info("GAME RESTARTED")
        self.is_paused = False
        self.reset()
