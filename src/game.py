from itertools import product

import arcade
import arcade.color as colors

from .agent import ResourcePile, Team, Village
from .config import GameConfig
from .constants import WINDOW_PADDING
from .game_map import GameMap
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
            height=height,
            title=title,
            samples=16,
        )
        Tile.width = (width - 2 * WINDOW_PADDING) / game_config.width
        Tile.height = Tile.width

        self.paused = False
        self.game_config = game_config
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

        print(f"Center of village 1: {village1_center}")
        print(f"Center of village 2: {village2_center}")

        village1 = Village(village1_center, Tiles.VILLAGE_1)
        village2 = Village(village2_center, Tiles.VILLAGE_2)

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

        team1 = Team(village1, team1_resources, Tiles.AGENT_1, config)
        team2 = Team(village2, team2_resources, Tiles.AGENT_2, config)
        self.teams = [team1, team2]

        for team in self.teams:
            self.map.generate_players(team, config.agents, config.map_price)

        self.map.print_map()

    def on_update(self, delta_time: float):
        if not self.paused:
            for team in self.teams:
                for agent in team.agents:
                    agent.update()

            for team in self.teams:
                if not team.resources.wanted_resources:
                    print(f"Team {team.id} Won!")
                    exit()

    def on_draw(self):
        for tile, tile_index in zip(self.tiles, self.map.matrix.flat):
            tile.set_tile_type(Tiles.get(tile_index))

        self.clear()
        self.shapes_list.draw()
        
        for tile in self.tiles:
            tile.render()

        for team in self.teams:
            team.render()

    def pause_game(self):
        print("GAME PAUSED")
        self.paused = True

    def resume_game(self):
        print("GAME RESUMED")
        self.paused = False

    def restart_game(self):
        print("GAME RESTARTED")
        self.paused = False
        self.reset()
