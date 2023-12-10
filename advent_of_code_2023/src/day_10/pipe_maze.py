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
    _nb_turns_right: int
    _nb_turns_left: int
    _state_grid: List[List[str]]
    _is_inside_on_the_right: bool

    def __init__(self,
                 grid: List[str]):
        self._grid = grid
        self._height = len(self._grid)
        self._width = len(self._grid[0])
        self._nb_turns_left = 0
        self._nb_turns_right = 0
        self._is_inside_on_the_right = True
        self._state_grid = [["."] * self._width for _row in range(self._height)]

    def _get_pipe(self,
                  position: Position) -> str:
        return self._grid[position.row][position.column]

    def _position_is_in_grid(self,
                             position: Position) -> bool:
        return 0 <= position.row < self._height and 0 <= position.column < self._width

    def get_main_loop_length(self) -> int:
        return len(self.get_main_loop()) - 1

    def get_main_loop(self) -> List[Position]:
        self._nb_turns_left = 0
        self._nb_turns_right = 0
        starting_position: Position = self.get_starting_position()
        direction: Position = self.get_a_starting_direction(starting_position)
        position: Position = starting_position + direction
        main_loop: List[Position] = [starting_position, position]
        while position != starting_position:
            direction = self.get_next_direction(position, direction)
            position += direction
            main_loop.append(position)
        return main_loop

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
                if (previous_direction == NORTH) != self._is_inside_on_the_right:
                    self._set_inside(position + WEST)
                else:
                    self._set_inside(position + EAST)
                return previous_direction
            case "-":
                if (previous_direction == EAST) != self._is_inside_on_the_right:
                    self._set_inside(position + NORTH)
                else:
                    self._set_inside(position + SOUTH)
                return previous_direction
            case "L":
                if (previous_direction == SOUTH) != self._is_inside_on_the_right:
                    self._set_inside(position + NORTH + EAST)
                else:
                    self._set_inside(position + WEST)
                    self._set_inside(position + SOUTH + WEST)
                    self._set_inside(position + SOUTH)
                if previous_direction == SOUTH:
                    self._nb_turns_left += 1
                    return EAST
                self._nb_turns_right += 1
                return NORTH
            case "F":
                if (previous_direction == NORTH) != self._is_inside_on_the_right:
                    self._set_inside(position + WEST)
                    self._set_inside(position + NORTH + WEST)
                    self._set_inside(position + NORTH)
                else:
                    self._set_inside(position + SOUTH + EAST)
                if previous_direction == NORTH:
                    self._nb_turns_right += 1
                    return EAST
                self._nb_turns_left += 1
                return SOUTH
            case "J":
                if (previous_direction == EAST) != self._is_inside_on_the_right:
                    self._set_inside(position + NORTH + WEST)
                else:
                    self._set_inside(position + SOUTH)
                    self._set_inside(position + SOUTH + EAST)
                    self._set_inside(position + EAST)
                if previous_direction == EAST:
                    self._nb_turns_left += 1
                    return NORTH
                self._nb_turns_right += 1
                return WEST
            case "7":
                if (previous_direction == EAST) != self._is_inside_on_the_right:
                    self._set_inside(position + NORTH)
                    self._set_inside(position + NORTH + EAST)
                    self._set_inside(position + EAST)
                else:
                    self._set_inside(position + SOUTH + WEST)
                if previous_direction == EAST:
                    self._nb_turns_right += 1
                    return SOUTH
                self._nb_turns_left += 1
                return WEST
        assert False, f"cannot get direction from {previous_direction} via {position}"

    def get_nb_enclosed_tiles(self) -> int:
        main_loop: List[Position] = self.get_main_loop()
        self._is_inside_on_the_right = self._nb_turns_right > self._nb_turns_left
        self._initialise_state_grid(main_loop)
        self.get_main_loop()
        self._flood_inside_tiles()
        return self._count_inside_tiles()

    def _initialise_state_grid(self,
                               main_loop: List[Position]):
        self._state_grid = [["."] * self._width for _row in range(self._height)]
        for position in main_loop:
            self._state_grid[position.row][position.column] = self._get_pipe(position)

    def _set_inside(self,
                    position: Position):
        if not self._position_is_in_grid(position):
            return
        if self._state_grid[position.row][position.column] == ".":
            self._state_grid[position.row][position.column] = "I"

    def _flood_inside_tiles(self):
        flooding_tiles: List[Position] = [Position(row, column)
                                          for row in range(self._height) for column in range(self._width)
                                          if self._state_grid[row][column] == "I"]
        while len(flooding_tiles) != 0:
            current_position = flooding_tiles.pop()
            for delta in [NORTH, EAST, SOUTH, WEST]:
                position = current_position + delta
                if self._position_is_in_grid(position):
                    if self._state_grid[position.row][position.column] == ".":
                        flooding_tiles.append(position)
                        self._set_inside(position)

    def _count_inside_tiles(self) -> int:
        return sum(sum(tile == "I" for tile in row) for row in self._state_grid)


def compute_farthest_distance(lines: List[str]) -> int:
    return int(Sketch(lines).get_main_loop_length() / 2)


def get_nb_enclosed_tiles(lines: List[str]) -> int:
    return Sketch(lines).get_nb_enclosed_tiles()
