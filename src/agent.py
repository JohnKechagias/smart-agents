from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, auto
from random import randint
from typing import Optional

from .config import GameConfig
from .map import Map
from .tiles import Tiles, TileType
from .types import Coords


class State(StrEnum):
    GATHERING_RESOURCE = auto()
    GATHERING_GOLD = auto()
    GATHERING_ENERGY_POT = auto()
    STORING_RESOURCE = auto()
    SEARCHING_FOR_RESOURCE = auto()
    SEARCHING_FOR_ENERGY_POT = auto()


class Energy(StrEnum):
    ENERGETIC = auto()
    EXCHAUSTED = auto()


@dataclass(frozen=True)
class Village:
    center: Coords
    tile: TileType
    radius: int = 10


@dataclass
class ResourcePile:
    def __init__(self, wood: int, iron: int, wheat: int):
        self.wanted_wood_count = wood
        self.wanted_iron_count = iron
        self.wanted_wheat_count = wheat
        self.wood = 0
        self.iron = 0
        self.wheat = 0
        self.wanted_resources: list[TileType] = []

        if wood > 0:
            self.wanted_resources.append(Tiles.WOOD)
        if iron > 0:
            self.wanted_resources.append(Tiles.IRON)
        if wheat > 0:
            self.wanted_resources.append(Tiles.WHEAT)

    def add(self, resource: TileType):
        if resource == Tiles.WOOD:
            self.wood += 1

            if (
                self.wood >= self.wanted_wood_count
                and Tiles.WOOD in self.wanted_resources
            ):
                self.wanted_resources.remove(Tiles.WOOD)
        elif resource == Tiles.IRON:
            self.iron += 1

            if (
                self.iron >= self.wanted_iron_count
                and Tiles.IRON in self.wanted_resources
            ):
                self.wanted_resources.remove(Tiles.IRON)
        elif resource == Tiles.WHEAT:
            self.wheat += 1

            if (
                self.wheat >= self.wanted_wheat_count
                and Tiles.WHEAT in self.wanted_resources
            ):
                self.wanted_resources.remove(Tiles.WHEAT)

    def is_needed(self, tile: TileType) -> bool:
        return tile in self.wanted_resources

    def __repr__(self) -> str:
        return f"ResourcePile(wood={self.wood}, iron={self.iron}, wheat={self.wheat})"


class Team:
    village: Village
    resources: ResourcePile
    agent_tile: TileType
    _id_counter = -1

    def __init__(
        self,
        village: Village,
        resources: ResourcePile,
        agent_tile: TileType,
        config: GameConfig,
    ):
        self.id = self.get_id()
        self.config = config
        self.village = village
        self.resources = resources
        self.agent_tile = agent_tile
        self.agents: list[Agent] = []
        self.targets = []

    @classmethod
    def get_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter

    def print_resources(self):
        print(f"Team {self.id} {self.resources}")


class Agent:
    _id_counter = -1

    def __init__(
        self,
        team: Team,
        map: Map,
        game_map: Map,
        position: Coords,
        map_price: int,
        move_range: int = 1,
    ):
        self.move_range = move_range
        self.id = self.get_id()
        self.team = team
        self.tile_type = team.agent_tile
        self.game_map = game_map
        self.map = map
        self.map_price = map_price

        self.state = State.SEARCHING_FOR_RESOURCE
        self.energy_state = Energy.ENERGETIC
        self.collected_resource = Tiles.EMPTY
        self.target: Coords = team.village.center
        self.visited_tiles: set[Coords] = set()
        self.has_explore_target = False

        self.gold = 0
        self._energy = 100
        self._position = position
        self._tile_standing_on = Tiles.EMPTY
        self.print_map()

    @classmethod
    def get_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter

    @property
    def position(self) -> Coords:
        return self._position

    @position.setter
    def position(self, value: Coords):
        for x in range(
            self.position.x - self.move_range, self.position.x + self.move_range + 1
        ):
            if x < 0 or x >= self.map.width:
                continue

            for y in range(
                self.position.y - self.move_range, self.position.y + self.move_range + 1
            ):
                if y < 0 or y >= self.map.height:
                    continue

                coords = Coords(x, y)
                tile = self.game_map.get_tile(coords)

                if tile in (Tiles.AGENT_1, Tiles.AGENT_2):
                    continue

                self.map.set_tile(coords, tile)

        self.visited_tiles.add(value)
        self.map.set_tile(self._position, self._tile_standing_on)
        self.game_map.set_tile(self._position, self._tile_standing_on)
        self._tile_standing_on = self.game_map.get_tile(value)
        self.game_map.set_tile(value, self.tile_type)
        self._position = value

    @property
    def tile(self) -> TileType:
        return self.map.get_tile(self.position)

    @tile.setter
    def tile(self, tile: TileType):
        self._tile_standing_on = tile
        self.map.set_tile(self.position, tile)

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, energy: int):
        self.energy_state = Energy.EXCHAUSTED if energy < 50 else Energy.ENERGETIC
        self._energy = energy

    def print_map(self):
        self.map.print(f"{self.id}_map.txt")

    def update(self):
        print(f"updating agent {self.id} of team {self.team.id}")
        if self.energy_state == Energy.EXCHAUSTED and self.state not in (
            State.GATHERING_ENERGY_POT,
            State.SEARCHING_FOR_ENERGY_POT,
        ):
            self.state = State.SEARCHING_FOR_ENERGY_POT
            print(f"agent {self.id} searches for energy pot. energy: {self.energy}")

        if self.game_map.get_tile(self.position) == Tiles.GOLD:
            self.pick_up_gold()

        elif self.gold > self.map_price:
            neighbor = self.get_neighboring_agent()

            if neighbor is not None:
                self.combine_maps(neighbor.map)
                neighbor.gold += self.map_price
                self.gold -= self.map_price

        elif self.state == State.SEARCHING_FOR_ENERGY_POT:
            print(f"agent {self.id} searches for energy pot. energy: {self.energy}")
            if self.locate_energy_pot():
                print(f"agent {self.id} is on his way to collect energy pot")
            elif not self.has_explore_target:
                self.set_explore_target()
                print(f"agent {self.id} is exploring")

            self.move_to_target()
        elif self.state == State.GATHERING_ENERGY_POT:
            self.gather_energy_pot()

        elif self.state == State.GATHERING_RESOURCE:
            self.gather_resource()

        elif self.state == State.STORING_RESOURCE:
            self.store_resource()

        elif self.state == State.SEARCHING_FOR_RESOURCE:
            if self.locate_resource():
                self.state = State.GATHERING_RESOURCE
            else:
                self.set_explore_target()

            self.move_to_target()

        self.energy -= 1

    def get_neighboring_agent(self) -> Optional[Agent]:
        for x in range(self.position.x - 1, self.position.x + 2):
            if x < 0 or x >= self.map.width:
                continue

            for y in range(self.position.y - 1, self.position.y + 2):
                if y < 0 or y >= self.map.height:
                    continue

                coords = Coords(x, y)
                if (
                    coords != self.position
                    and self.game_map.get_tile(coords) == self.team.agent_tile
                ):
                    for agent in self.team.agents:
                        if agent.position == coords:
                            return agent

    def gather_energy_pot(self):
        if self.position == self.target:
            if self._tile_standing_on != Tiles.ENERGY_POT:
                self.state = State.SEARCHING_FOR_ENERGY_POT
                return

            self.pick_up_energy_pot()
            self.state = State.SEARCHING_FOR_RESOURCE
        else:
            self.move_to_target()

    def locate_energy_pot(self):
        located_energy_pot = self.locate_tile(Tiles.ENERGY_POT)
        if located_energy_pot:
            self.state = State.GATHERING_ENERGY_POT
        else:
            self.set_explore_target()

        return located_energy_pot

    def locate_tile(self, tile_to_locate: TileType) -> bool:
        for pos in self.map.positions:
            tile = self.map.get_tile(pos)
            if tile == tile_to_locate:
                self.has_explore_target = False
                self.target = pos
                self.team.targets.append(pos)
                return True
        return False

    def locate_resource(self) -> bool:
        for pos in self.map.positions:
            tile = self.map.get_tile(pos)
            if self.team.resources.is_needed(tile) and pos not in self.team.targets:
                self.target = pos
                self.team.targets.append(pos)
                self.has_explore_target = False
                self.state = State.GATHERING_RESOURCE
                return True
        return False

    def gather_resource(self):
        if self.position == self.target:
            if not self.team.resources.is_needed(self._tile_standing_on):
                self.state = State.SEARCHING_FOR_RESOURCE
                return

            self.pick_up_resource()
        else:
            self.move_to_target()

    def store_resource(self):
        if self.tile == self.team.village.tile:
            print(f"agent {self.id} stored resource {self.collected_resource}")
            self.team.resources.add(self.collected_resource)
            self.collected_resource = Tiles.EMPTY
            self.state = State.SEARCHING_FOR_RESOURCE
            self.locate_resource()
        else:
            self.move_to_target()

    def move_to_target(self):
        scores = []
        for x in range(
            self.position.x - self.move_range, self.position.x + self.move_range + 1
        ):
            if x < 0 or x >= self.map.width:
                continue

            for y in range(
                self.position.y - self.move_range, self.position.y + self.move_range + 1
            ):
                if y < 0 or y >= self.map.height:
                    continue

                score = abs(self.target.x - x) + abs(self.target.y - y)
                coords = Coords(x, y)
                scores.append((coords, score))

        scores.sort(key=lambda entry: entry[1])
        for hop_coords, _ in scores:
            curr_tile = self.game_map.get_tile(hop_coords)
            is_hope_target_agent = curr_tile in (Tiles.AGENT_1, Tiles.AGENT_2)
            if hop_coords in self.visited_tiles or is_hope_target_agent:
                continue

            print(f"agent {self.id} moved from {self.position} to {hop_coords}")
            self.position = hop_coords
            return

        self.visited_tiles.clear()

    def pick_up_energy_pot(self):
        print(f"agent {self.id} picked up energy pot")
        self.tile = Tiles.EMPTY
        new_energy_bar = self._energy + self.team.config.energy_pots_energy
        self._energy = min(new_energy_bar, 100)
        self.visited_tiles.clear()

    def pick_up_gold(self):
        print(f"agent {self.id} picked up gold")
        self.tile = Tiles.EMPTY
        self.gold += 1

    def pick_up_resource(self):
        print(f"agent {self.id} picked up resource {self.tile.name}")
        self.collected_resource = self.tile
        self.tile = Tiles.EMPTY
        self.visited_tiles.clear()
        self.locate_tile(self.team.village.tile)
        self.team.targets.remove(self.position)
        self.state = State.STORING_RESOURCE

    def buy_energy_pot(self):
        print(f"agent {self.id} bought energy pot")
        self.gold -= self.team.config.energy_pot_price
        new_energy_bar = self._energy + self.team.config.energy_pots_energy
        self._energy = min(new_energy_bar, 100)
        self.visited_tiles.clear()

    def buy_map(self, map: Map):
        print(f"agent {self.id} bought a map")
        self.gold -= self.team.config.map_price
        for pos in self.map.positions:
            tile = self.map.get_tile(pos)
            if tile == Tiles.UNKNOWN:
                tile_to_set = map.get_tile(pos)
                self.map.set_tile(pos, tile_to_set)

            if map.get_tile(pos) == Tiles.EMPTY:
                self.map.set_tile(pos, Tiles.EMPTY)

    def set_explore_target(self):
        unknown_block_index = randint(0, self.map.size - 1)
        unknown_blocks_positions = []

        for pos in self.map.positions:
            if self.map.get_tile(pos) == Tiles.UNKNOWN:
                unknown_blocks_positions.append(pos)

            if len(unknown_blocks_positions) > unknown_block_index:
                self.target = pos
                self.has_explore_target = True
                return

        random_unknown_block_index = unknown_block_index % len(unknown_blocks_positions)
        self.target = unknown_blocks_positions[random_unknown_block_index]
        self.has_explore_target = True

    def combine_maps(self, map: Map):
        for pos in self.map.positions:
            new_tile = map.get_tile(pos)
            if self.map.get_tile(pos) == Tiles.UNKNOWN and new_tile != Tiles.UNKNOWN:
                self.map.set_tile(pos, new_tile)
