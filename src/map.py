import math
import random

import numpy as np

from .constants import Position, Tile, Tiles, Map
from .agent import Team
from math import floor


class GameMap(Map):
    variance = 4
    village_radius = 10

    def __init__(
        self,
        width: int,
        height: int,
        wood: int,
        iron: int,
        wheat: int,
        gold: int,
        energy_pots: int,
        team1: Team,
        team2: Team,
    ):
        matrix = np.zeros((height, width), dtype=int)
        super().__init__(matrix)

        self.width = width
        self.height = height
        self.total_blocks = self.width * self.height
        self.village_1_center = Position(0, 0)
        self.village_2_center = Position(0, 0)

        self.generate_teams(team1, team2)
        self.generate_resources(wood, iron, wheat)
        self.generate_gold(gold)
        self.generate_energy_pots(energy_pots)
        self.print_map()

    def generate_teams(self, *teams):
        for team in teams:
            self.generate_village(
                team.village.center,
                len(team.agents),
                team.village.tile,
            )
            self.generate_players(team)

    def get_variance(self) -> int:
        return random.randint(-(self.variance // 2), self.variance // 2)

    def generate_players(self, team: Team):
        for agent in team.agents:
            pos = self.get_unpopulated_block_inside_village(
                team.village.center, self.village_radius
            )
            self.set_tile(pos, agent.tile_symbol)
            agent.position = pos

    def get_unpopulated_block_inside_village(
        self,
        center: Position,
        radius: int,
    ) -> Position:
        x, y = center.x, center.y
        while self.get_tile(Position(x, y)) != Tiles.EMPTY:
            x = center.x + floor(radius * (random.randint(-100, 100) / 100))
            y = center.y + floor(radius * (random.randint(-100, 100) / 100))
        return Position(x, y)

    def generate_resources(self, wood: int, iron: int, wheat: int):
        self.generate_resource(wood, Tiles.WOOD)
        self.generate_resource(iron, Tiles.IRON)
        self.generate_resource(wheat, Tiles.WHEAT)

    def generate_gold(self, gold: int):
        for _ in range(gold):
            pos = self.get_unpopulated_block()
            self.set_tile(pos, Tiles.GOLD)

    def generate_energy_pots(self, energy_pots: int):
        for _ in range(energy_pots):
            pos = self.get_unpopulated_block()
            self.set_tile(pos, Tiles.ENERGY_POT)

    def generate_resource(self, resource_percentage: int, resource: Tile):
        total_resource_blocks = (resource_percentage * self.total_blocks) // 100
        for _ in range(total_resource_blocks):
            pos = self.get_unpopulated_block()
            self.set_tile(pos, resource)

    def get_unpopulated_block(self) -> Position:
        pos = Position(0, 0)
        while self.get_tile(pos) != Tiles.EMPTY:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            pos = Position(x, y)
        return pos

    def generate_village(self, center: Position, agents: int, tile: Tile):
        for index in range(agents):
            angle = (2 * math.pi / agents) * index
            house_x = center.x + math.floor(math.cos(angle) * self.village_radius)
            house_y = center.y + math.floor(math.sin(angle) * self.village_radius)
            self.generate_house(house_x, house_y, tile)

    def generate_house(self, x: int, y: int, tile: Tile):
        x += self.get_variance()
        y += self.get_variance()
        for i in range(-1, 2):
            for j in range(-1, 2):
                pos = Position(x + i, y + j)
                self.set_tile(pos, tile)

    def print_map(self):
        with open("map.txt", "w") as f:
            for i in range(self.width):
                for j in range(self.height):
                    symbol = Tiles.get(self.matrix[j][i]).symbol
                    f.write(symbol)

                f.write("\n")
