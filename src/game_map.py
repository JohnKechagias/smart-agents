import math
import random
from math import floor

import numpy as np

from .agent import Agent, Team, Village
from .map import Map
from .tiles import Tiles, TileType
from .types import Coords


class GameMap(Map):
    variance = 4

    def __init__(
        self,
        width: int,
        height: int,
        wood: int,
        iron: int,
        wheat: int,
        gold: int,
        energy_pots: int,
        villages: list[Village],
        num_of_players: int,
    ):
        matrix = np.zeros((height, width), dtype=int)
        super().__init__(matrix)
        self.village_radius = math.floor(0.1 * height)

        for village in villages:
            self.generate_village(village, num_of_players)

        self.generate_resources(wood, iron, wheat)
        self.generate_gold(gold)
        self.generate_energy_pots(energy_pots)

    def get_variance(self) -> int:
        return random.randint(-(self.variance // 2), self.variance // 2)

    def generate_players(self, team: Team, num_of_players: int, map_price: int):
        center = team.village.center
        radius = self.village_radius

        for _ in range(num_of_players):
            position = self.get_unpopulated_tile_inside_village(center, radius)
            self.set_tile(position, team.agent_tile)
            agent_map = np.full(
                [self.width, self.height], Tiles.UNKNOWN.index, dtype=np.int8
            )

            for pos in self.positions:
                x_inside_village = center.x - radius <= pos.x <= center.x + radius
                y_inside_village = center.y - radius <= pos.y <= center.y + radius
                if x_inside_village and y_inside_village:
                    agent_map[pos.x][pos.y] = self.matrix[pos.x][pos.y]

            move_range = 2 if team.agent_tile == Tiles.AGENT_2 else 1
            agent = Agent(team, Map(agent_map), self, position, map_price, move_range)
            team.agents.append(agent)

    def get_unpopulated_tile_inside_village(
        self, center: Coords, radius: int
    ) -> Coords:
        pos = center
        iterations: int = 0
        max_iterations_with_given_radius = 100

        while self.get_tile(pos) != Tiles.EMPTY:
            if iterations > max_iterations_with_given_radius:
                radius += 1
                iterations = 0

            x = center.x + floor(radius * (random.randint(-100, 100) / 100))
            y = center.y + floor(radius * (random.randint(-100, 100) / 100))
            pos = Coords(x, y)
            iterations += 1
        return pos

    def generate_resources(self, wood: int, iron: int, wheat: int):
        self.generate_resource(wood, Tiles.WOOD)
        self.generate_resource(iron, Tiles.IRON)
        self.generate_resource(wheat, Tiles.WHEAT)

    def generate_gold(self, gold: int):
        for _ in range(gold):
            pos = self.get_unpopulated_tile()
            self.set_tile(pos, Tiles.GOLD)

    def generate_energy_pots(self, energy_pots: int):
        for _ in range(energy_pots):
            pos = self.get_unpopulated_tile()
            self.set_tile(pos, Tiles.ENERGY_POT)

    def generate_resource(self, resource_percentage: int, resource: TileType):
        total_resource_tiles = (resource_percentage * self.size) // 100
        for _ in range(total_resource_tiles):
            pos = self.get_unpopulated_tile()
            self.set_tile(pos, resource)

    def get_unpopulated_tile(self) -> Coords:
        pos = Coords(0, 0)
        while self.get_tile(pos) != Tiles.EMPTY:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            pos = Coords(x, y)
        return pos

    def generate_village(self, village: Village, num_of_players: int):
        center = village.center
        for index in range(num_of_players):
            angle = (2 * math.pi / num_of_players) * index
            house_x = center.x + math.floor(math.cos(angle) * self.village_radius)
            house_y = center.y + math.floor(math.sin(angle) * self.village_radius)
            self.generate_house(house_x, house_y, village.tile)

    def generate_house(self, x: int, y: int, tile: TileType):
        x += self.get_variance()
        y += self.get_variance()
        for i in range(-1, 2):
            for j in range(-1, 2):
                pos = Coords(x + i, y + j)
                self.set_tile(pos, tile)

    def print_map(self):
        super().print("gamemap.txt")
