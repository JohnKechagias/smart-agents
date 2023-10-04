import numpy as np
from dataclasses import dataclass
from enum import Enum, auto
from .constants import Position, Tile, Tiles, Map


class State(Enum):
    GATHERING_RESOURCE = auto()
    GATHERING_ENERGY_POT = auto()
    STORING_RESOURCE = auto()
    EXPORING = auto()


class EnergyState(Enum):
    ENERGETIC = auto()
    TIRED = auto()
    EXCHAUSTED = auto()


@dataclass
class Village:
    center: Position
    tile: Tile


@dataclass
class ResourcePile:
    def __init__(self, wood: int, iron: int, wheat: int):
        self.wanted_wood_count = wood
        self.wanted_iron_count = iron
        self.wanted_wheat_count = wheat
        self.wood = 0
        self.iron = 0
        self.wheat = 0

        self.wanted_resources = [
            Tiles.WOOD,
            Tiles.IRON,
            Tiles.WHEAT,
        ]

    def add(self, resource: Tile):
        resource_mapper = {
            Tiles.WOOD.index: self.wood,
            Tiles.IRON.index: self.iron,
            Tiles.WHEAT.index: self.wheat,
        }
        resource_mapper[resource.index] += 1

        if resource == Tiles.WOOD and self.wood >= self.wanted_wood_count:
            self.wanted_resources.remove(Tiles.WOOD)
        elif resource == Tiles.IRON and self.iron >= self.wanted_iron_count:
            self.wanted_resources.remove(Tiles.IRON)
        elif resource == Tiles.WHEAT and self.wheat >= self.wanted_wheat_count:
            self.wanted_resources.remove(Tiles.WHEAT)

    def is_needed(self, tile: Tile) -> bool:
        return tile in self.wanted_resources


class Team:
    village: Village
    resources: ResourcePile
    agent_tile: Tile

    def __init__(self, village: Village, resources: ResourcePile,  agents: int, agent_tile: Tile):
        self.village = village
        self.resources = resources
        self.agents = [Agent(self, agent_tile) for _ in range(agents)]


class Agent:
    def __init__(self, team: Team, tile: Tile):
        self.team = team
        self.map = Map(np.zeros([10, 10]))
        self.state = State.EXPORING
        self.energy = EnergyState.ENERGETIC
        self.collected_resource = Tiles.EMPTY
        self.position = team.village.center
        self.target: Position = team.village.center
        self.visited_tiles: list[Position] = []
        self.tile_symbol = tile

    @property
    def tile(self) -> Tile:
        return self.map.get_tile(self.position)

    @tile.setter
    def tile(self, tile: Tile):
        self.map.set_tile(self.position, tile)

    def update(self):
        if self.state == State.GATHERING_RESOURCE:
            if self.position != self.target:
                self.move_to_target()
                return

            self.pick_up_resource()
        elif self.state == State.STORING_RESOURCE:
            if self.tile != self.team.village.tile:
                self.move_to_target()
                return

            self.team.resources.add(self.collected_resource)
            self.collected_resource = Tiles.EMPTY
            self.state = (
                State.GATHERING_RESOURCE if self.can_find_resource() else State.EXPORING
            )

        elif self.state == State.EXPORING:
            self.explore()
            for i in range(self.map.matrix.shape[0]):
                for j in range(self.map.matrix.shape[1]):
                    pos = Position(i, j)
                    if self.map.get_tile(pos) in (
                        Tiles.WHEAT,
                        Tiles.GOLD,
                        Tiles.WOOD,
                    ):
                        self.target = pos
                        self.state = State.GATHERING_RESOURCE
                        return

    def move_to_target(self):
        scores = []
        for x in range(self.position.x - 1, self.position.x + 2):
            for y in range(self.position.y - 1, self.position.y + 2):
                scores.append(
                    (Position(x, y), abs(self.target.x - x) + abs(self.target.y - y))
                )

        scores.sort(key=lambda entry: entry[1])
        for hop_candidate in scores:
            if hop_candidate[0] not in self.visited_tiles:
                self.visited_tiles.append(hop_candidate[0])
                self.position = scores[0]
                return

    def pick_up_energy_pot(self):
        pass

    def pick_up_gold(self):
        pass

    def pick_up_resource(self):
        self.collected_resource = self.tile
        self.tile = Tiles.EMPTY
        self.visited_tiles.clear()
        self.action = State.STORING_RESOURCE
        self.target = self.team.village.center

    def buy_energy_pot(self):
        pass

    def buy_map(self):
        pass

    def can_find_resource(self) -> bool:
        for i in range(self.map.matrix.shape[0]):
            for j in range(self.map.matrix.shape[1]):
                if self.team.resources.is_needed(Tiles.get(self.map.matrix[i][j])):
                    self.target = Position(i, j)
                    return True
        return False

    def explore(self):
        ...
