# 35min : Bois 2
# 50min : Bronze 846
# 1h10 : Bronze 822
# 2h : Bronze 863

# TODO:
# Switch type is opponent pac nearby
# Maintain grid step:
#   start: all cells are unknown
#   each turn:
#     clear cells seen by pac
#     fill cells from input
# For each pac, test 4 directions.
#   Evaluate each resulting position:
#     Flood
#       Handle moves across limits (also for testing 4 directions)
#     Value of pellet divided by distance
#     Value for unknown cell
#     Value for opponent pac that can be eaten
# Handle turn with speed only: keep in mind previously targeted pellets


from __future__ import annotations
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Final


def debug(message: str):
    print(message, file=sys.stderr, flush=True)


@dataclass(frozen=True, order=True)
class Position:
    row: int
    column: int

    def __add__(self,
                other: Position) -> Position:
        return Position(self.row + other.row, self.column + other.column)

    def __mul__(self,
                factor: int) -> Position:
        return Position(self.row * factor, self.column * factor)

    def __repr__(self):
        return f"({self.row}, {self.column})"

    def manhattan_distance(self,
                           other: Position) -> int:
        return abs(self.row - other.row) + abs(self.column - other.column)

    def opposite(self) -> Position:
        return Position(- self.row, - self.column)


NIL_POSITION: Final[Position] = Position(0, 0)
NORTH: Final[Position] = Position(-1, 0)
EAST: Final[Position] = Position(0, 1)
SOUTH: Final[Position] = Position(1, 0)
WEST: Final[Position] = Position(0, -1)
ALL_DIRECTIONS: Final[list[Position]] = [NORTH, EAST, SOUTH, WEST]


class Grid:
    width: int = 0
    height: int = 0
    rows: list[str]

    def init_from_input(self):
        # width: size of the grid
        # height: top left corner is (x=0, y=0)
        self.width, self.height = [int(i) for i in input().split()]
        self.rows = []
        for i in range(self.height):
            row = input()  # one line of the grid: space " " is floor, pound "#" is wall
            self.rows.append(row)


@dataclass(frozen=True, order=True)
class Pac:
    pac_id: int = 0
    mine: bool = True
    position: Position = NIL_POSITION
    type_id: str = ""
    speed_turns_left: int = 0
    ability_cooldown: int = 0

    @staticmethod
    def get_pac_from_input() -> Pac:
        inputs = input().split()
        pac_id = int(inputs[0])  # pac number (unique within a team)
        mine = inputs[1] != "0"  # true if this pac is yours
        row = int(inputs[2])  # position in the grid
        column = int(inputs[3])  # position in the grid
        type_id = inputs[4]  # unused in wood leagues
        speed_turns_left = int(inputs[5])  # unused in wood leagues
        ability_cooldown = int(inputs[6])  # unused in wood leagues
        return Pac(
            pac_id=pac_id,
            mine=mine,
            position=Position(row, column),
            type_id=type_id,
            speed_turns_left=speed_turns_left,
            ability_cooldown=ability_cooldown
        )


@dataclass(frozen=True, order=True)
class Pellet:
    position: Position = NIL_POSITION
    value: int = 0

    @staticmethod
    def get_pellet_from_input() -> Pellet:
        row, column, value = [int(j) for j in input().split()]
        return Pellet(position=Position(row, column), value=value)


class State:
    my_score: int = 0
    opponent_score: int = 0
    pac_list: list[Pac]
    pellet_list: list[Pellet]

    def init_from_input(self):
        self.my_score, self.opponent_score = [int(i) for i in input().split()]
        visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
        self.pac_list = [Pac.get_pac_from_input() for i in range(visible_pac_count)]
        visible_pellet_count = int(input())  # all pellets in sight
        self.pellet_list = [Pellet.get_pellet_from_input() for i in range(visible_pellet_count)]

    def get_pac_by_id(self,
                      mine: bool,
                      pac_id: int) -> Pac:
        for pac in self.pac_list:
            if pac.mine == mine and pac.pac_id == pac_id:
                return pac
        raise RuntimeError(f"Pac {mine} {pac_id} not found")


class Solver:
    grid: Grid
    state: State
    targeted_pellets: list[Pellet]

    def __init__(self,
                 grid: Grid,
                 state: State):
        self.grid = grid
        self.state = state

    def get_moves(self) -> list[str]:
        self.targeted_pellets = []
        target_pellet_per_pac: dict[Pac, Pellet] = {
            pac: self.find_closest_pellet(pac) for pac in self.state.pac_list if pac.mine}
        self.solve_common_targets(target_pellet_per_pac)
        return self.get_moves_from_targets(target_pellet_per_pac)

    def find_closest_pellet(self,
                            pac: Pac) -> Pellet:
        closest_pellet: Pellet = Pellet()
        shortest_distance: float = 1000.0
        for pellet in self.state.pellet_list:
            if pellet in self.targeted_pellets:
                continue
            distance = float(pac.position.manhattan_distance(pellet.position)) / pellet.value
            if distance < shortest_distance:
                shortest_distance = distance
                closest_pellet = pellet
        return closest_pellet

    def solve_common_targets(self,
                             target_pellet_per_pac: dict[Pac, Pellet]):
        pac_list_per_target_pellet = defaultdict(list)
        for pac, pellet in target_pellet_per_pac.items():
            pac_list_per_target_pellet[pellet].append(pac)
        self.targeted_pellets = list(pac_list_per_target_pellet.keys())
        for pellet, pac_list in pac_list_per_target_pellet.items():
            if len(pac_list) > 2:
                shortest_distance: float = 1000.0
                for pac in pac_list:
                    distance = float(pellet.position.manhattan_distance(pac.position)) \
                        + (float(pac.pac_id) / 10)
                    shortest_distance = min(shortest_distance, distance)
                for pac in pac_list:
                    distance = float(pellet.position.manhattan_distance(pac.position)) \
                        + (float(pac.pac_id) / 10)
                    if distance > shortest_distance:
                        target_pellet_per_pac[pac] = self.find_closest_pellet(pac)

    def get_moves_from_targets(self,
                               target_pellet_per_pac: dict[Pac, Pellet]) -> list[str]:
        return [self.get_pac_action(pac, pellet) for pac, pellet in target_pellet_per_pac.items()]

    def get_pac_action(self,
                       pac: Pac,
                       target_pellet: Pellet) -> str:
        if self.should_speed(pac, target_pellet):
            return f"SPEED {pac.pac_id} rush to {target_pellet.position}"
        return f"MOVE {pac.pac_id} {target_pellet.position.row} {target_pellet.position.column}" \
               + f" go for {target_pellet.position}"

    @staticmethod
    def should_speed(pac: Pac,
                     target_pellet: Pellet) -> bool:
        distance: int = pac.position.manhattan_distance(target_pellet.position)
        return distance > 2 \
            and float(target_pellet.value) / distance > 1.5 \
            and pac.speed_turns_left == 0 \
            and pac.ability_cooldown == 0


def main():
    grid: Grid = Grid()
    grid.init_from_input()
    while True:
        state: State = State()
        state.init_from_input()
        solver: Solver = Solver(grid, state)
        moves: list[str] = solver.get_moves()
        concatenated_moves = " | ".join(moves)
        print(concatenated_moves)


if __name__ == '__main__':
    main()
