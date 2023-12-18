from typing import Final

from src.util.position import Position, NORTH, EAST, SOUTH, WEST, ALL_DIRECTIONS


DIRECTION_PER_CHAR: Final[dict[str, Position]] = {
    "U": NORTH,
    "D": SOUTH,
    "R": EAST,
    "L": WEST
}


class Lagoon:
    grid: dict[Position, str]
    min_row: int
    max_row: int
    min_column: int
    max_column: int

    def __init__(self,
                 digger_directions: list[str]):
        self.grid = {}
        self.dig(digger_directions)
        self.fill_inside_trench()
        # self.print_grid()

    def get_cell(self,
                 position: Position) -> str:
        return self.grid.get(position, " ")

    def print_grid(self):
        for row in range(self.min_row, self.max_row + 1):
            print("".join(self.get_cell(Position(row, column))
                          for column in range(self.min_column, self.max_column + 1)))

    def dig(self,
            digger_directions: list[str]):
        position: Position = Position(0, 0)
        self.grid[position] = "#"
        for instruction in digger_directions:
            direction_char, length, _ = instruction.split()
            direction: Position = DIRECTION_PER_CHAR[direction_char]
            for _ in range(int(length)):
                position += direction
                self.grid[position] = "#"
        self.min_row = min(position.row for position in self.grid)
        self.max_row = max(position.row for position in self.grid)
        self.min_column = min(position.column for position in self.grid)
        self.max_column = max(position.column for position in self.grid)

    def fill_inside_trench(self):
        propagation_queue: list[Position] = [self.get_first_inside_cell()]
        while propagation_queue:
            position = propagation_queue.pop()
            if self.get_cell(position) == "#":
                continue
            self.grid[position] = "#"
            for direction in ALL_DIRECTIONS:
                propagation_queue.append(position + direction)

    def get_first_inside_cell(self):
        column: int = next(column for column in range(self.min_column, self.max_column)
                           if self.get_cell(Position(0, column)) == "#")
        return Position(0, column) + SOUTH + EAST

    def get_capacity(self) -> int:
        return len(self.grid)


def compute_lagoon_capacity(lines: list[str]) -> int:
    return Lagoon(lines).get_capacity()


class Lagoon2:
    grid: dict[Position, str]

    def __init__(self,
                 digger_directions: list[str]):
        self.grid = {}
        self.dig(digger_directions)
        self.fill_inside_trench()
        # self.print_grid()

    def get_cell(self,
                 position: Position) -> str:
        return self.grid.get(position, " ")

    def print_grid(self):
        for row in range(self.min_row, self.max_row + 1):
            print("".join(self.get_cell(Position(row, column))
                          for column in range(self.min_column, self.max_column + 1)))

    def dig(self,
            digger_directions: list[str]):
        position: Position = Position(0, 0)
        self.grid[position] = "#"
        for instruction in digger_directions:
            direction_char, length, _ = instruction.split()
            direction: Position = DIRECTION_PER_CHAR[direction_char]
            for _ in range(int(length)):
                position += direction
                self.grid[position] = "#"
        self.min_row = min(position.row for position in self.grid)
        self.max_row = max(position.row for position in self.grid)
        self.min_column = min(position.column for position in self.grid)
        self.max_column = max(position.column for position in self.grid)

    def fill_inside_trench(self):
        propagation_queue: list[Position] = [self.get_first_inside_cell()]
        while propagation_queue:
            position = propagation_queue.pop()
            if self.get_cell(position) == "#":
                continue
            self.grid[position] = "#"
            for direction in ALL_DIRECTIONS:
                propagation_queue.append(position + direction)

    def get_first_inside_cell(self):
        column: int = next(column for column in range(self.min_column, self.max_column)
                           if self.get_cell(Position(0, column)) == "#")
        return Position(0, column) + SOUTH + EAST

    def get_capacity(self) -> int:
        return len(self.grid)


def compute_lagoon_capacity_triangle_formula(lines: list[str],
                                             second_part: bool = False) -> int:
    inner_area: float = 0
    perimeter: int = 0
    position: Position = Position(0, 0)
    previous_position: Position = position
    for line in lines:
        direction_char, length = get_direction_and_length(line, second_part)
        direction: Position = DIRECTION_PER_CHAR[direction_char]
        position = position + direction * length
        inner_area += (previous_position.row * position.column - position.row * previous_position.column) / 2
        perimeter += length
        previous_position = position
    area = int(abs(inner_area)) + int(perimeter / 2) + 1
    return int(area)


def get_direction_and_length(line: str,
                             second_part: bool = False) -> tuple[str, int]:
    if not second_part:
        direction, length_str, _ = line.split()
        return direction, int(length_str)
    color = line.split("#")[1][:-1]
    length: int = int(color[:-1], 16)
    direction = "RDLU"[int(color[-1])]
    return direction, length
