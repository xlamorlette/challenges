# 35min -> Bois 2
# 50min -> Bronze

# TODO:
# Handle moves across limits
# Don't target same pellet: store already targeted pellets

from __future__ import annotations
from dataclasses import dataclass
from typing import Final


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


class Pac:
    pac_id: int = 0
    mine: bool = True
    position: Position = NIL_POSITION
    type_id: str = ""
    speed_turns_left: int = 0
    ability_cooldown: int = 0

    def init_from_input(self):
        inputs = input().split()
        self.pac_id = int(inputs[0])  # pac number (unique within a team)
        self.mine = inputs[1] != "0"  # true if this pac is yours
        row = int(inputs[2])  # position in the grid
        column = int(inputs[3])  # position in the grid
        self.position = Position(row, column)
        self.type_id = inputs[4]  # unused in wood leagues
        self.speed_turns_left = int(inputs[5])  # unused in wood leagues
        self.ability_cooldown = int(inputs[6])  # unused in wood leagues


class Pellet:
    position: Position = NIL_POSITION
    value: int = 0

    def init_from_input(self):
        row, column, self.value = [int(j) for j in input().split()]
        self.position = Position(row, column)


class State:
    my_score: int = 0
    opponent_score: int = 0
    pac_list: list[Pac]
    pellet_list: list[Pellet]

    def init_from_input(self):
        self.my_score, self.opponent_score = [int(i) for i in input().split()]

        self.pac_list = []
        visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
        for i in range(visible_pac_count):
            pac = Pac()
            pac.init_from_input()
            self.pac_list.append(pac)

        self.pellet_list = []
        visible_pellet_count = int(input())  # all pellets in sight
        for i in range(visible_pellet_count):
            pellet = Pellet()
            pellet.init_from_input()
            self.pellet_list.append(pellet)


class Solver:
    grid: Grid
    state: State

    def __init__(self,
                 grid: Grid,
                 state: State):
        self.grid = grid
        self.state = state

    def get_moves(self) -> list[str]:
        moves: list[str] = []
        for pac in self.state.pac_list:
            if pac.mine:
                pellet: Pellet = self.find_closest_pellet(pac)
                moves.append(f"MOVE {pac.pac_id} {pellet.position.row} {pellet.position.column}")
        return moves

    def find_closest_pellet(self,
                            pac: Pac) -> Pellet:
        closest_pellet: Pellet = Pellet()
        shortest_distance: float = 1000.0
        for pellet in self.state.pellet_list:
            distance = float(pac.position.manhattan_distance(pellet.position)) / pellet.value
            if distance < shortest_distance:
                shortest_distance = distance
                closest_pellet = pellet
        return closest_pellet


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
