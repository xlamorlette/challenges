from __future__ import annotations
from dataclasses import dataclass
from typing import Final, List


@dataclass
class Position:
    row: int
    column: int

    def __add__(self,
                other: Position) -> Position:
        return Position(self.row + other.row, self.column + other.column)


NORTH: Final[Position] = Position(-1, 0)
EAST: Final[Position] = Position(0, 1)
SOUTH: Final[Position] = Position(1, 0)
WEST: Final[Position] = Position(0, -1)


class Sketch:
    _grid: List[str]
    _height: int
    _width: int

    def __init__(self,
                 grid: List[str]):
        self._grid = grid
        self._height = len(self._grid)
        self._width = len(self._grid[0])

    def _get_pipe(self,
                  position: Position) -> str:
        return self._grid[position.row][position.column]

    def get_main_loop_length(self) -> int:
        starting_position: Position = self.get_starting_position()
        direction: Position = self.get_a_starting_direction(starting_position)
        position: Position = starting_position + direction
        loop_length: int = 1
        while position != starting_position:
            direction = self.get_next_direction(position, direction)
            position += direction
            loop_length += 1
        return loop_length

    def get_starting_position(self) -> Position:
        for row in range(self._height):
            for column in range(self._width):
                if self._grid[row][column] == "S":
                    return Position(row, column)
        assert False, "starting position not found"

    def get_a_starting_direction(self,
                                 starting_position: Position) -> Position:
        if starting_position.column < self._width - 1:
            position = starting_position + EAST
            if self._get_pipe(position) in ["-", "J", "7"]:
                return EAST
        if starting_position.column > 0:
            position = starting_position + WEST
            if self._get_pipe(position) in ["-", "L", "F"]:
                return WEST
        if starting_position.row < self._height - 1:
            position = starting_position + SOUTH
            if self._get_pipe(position) in ["|", "J", "L"]:
                return SOUTH
        if starting_position.row > 0:
            position = starting_position + NORTH
            if self._get_pipe(position) in ["|", "7", "F"]:
                return NORTH
        assert False, f"starting direction not found from {starting_position}"

    def get_next_direction(self,
                           position: Position,
                           previous_direction: Position) -> Position:
        match self._get_pipe(position):
            case "|":
                return previous_direction
            case "-":
                return previous_direction
            case "L":
                return EAST if previous_direction == SOUTH else NORTH
            case "F":
                return EAST if previous_direction == NORTH else SOUTH
            case "J":
                return NORTH if previous_direction == EAST else WEST
            case "7":
                return SOUTH if previous_direction == EAST else WEST
        assert False, f"cannot get direction from {previous_direction} via {position}"


def compute_farthest_distance(lines: List[str]) -> int:
    return int(Sketch(lines).get_main_loop_length() / 2)
