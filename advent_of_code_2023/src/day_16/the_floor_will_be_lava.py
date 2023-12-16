from typing import List, Set, Tuple

from src.util.position import Position, NORTH, SOUTH, EAST, WEST


Direction = Position
PositionAndDirection = Tuple[Position, Direction]


class Contraption:
    grid: List[List[str]]
    height: int
    width: int
    visited_cells: List[List[Set[Direction]]]

    def __init__(self,
                 lines: List[str]):
        self.grid = [list(line) for line in lines]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def propagate_beam(self):
        self.visited_cells = [[set() for _column in range(self.width)] for _row in range(self.height)]
        self.visited_cells[0][0].add(EAST)
        propagation_list: List[PositionAndDirection] = [(Position(0, 0), EAST)]
        while len(propagation_list) > 0:
            next_cells: List[PositionAndDirection] = self.get_next_cells(*propagation_list.pop())
            for cell, direction in next_cells:
                if direction not in self.visited_cells[cell.row][cell.column]:
                    self.visited_cells[cell.row][cell.column].add(direction)
                    propagation_list.append((cell, direction))

    def get_next_cells(self,
                       position: Position,
                       direction: Direction) -> List[PositionAndDirection]:
        next_cells: List[PositionAndDirection] = []
        cell = self.grid[position.row][position.column]
        if cell == "-" and direction in [NORTH, SOUTH]:
            next_cells.append((position + EAST, EAST))
            next_cells.append((position + WEST, WEST))
        elif cell == "|" and direction in [WEST, EAST]:
            next_cells.append((position + NORTH, NORTH))
            next_cells.append((position + SOUTH, SOUTH))
        elif cell == "\\":
            next_direction = {NORTH: WEST, EAST: SOUTH, SOUTH: EAST, WEST: NORTH}[direction]
            next_cells.append((position + next_direction, next_direction))
        elif cell == "/":
            next_direction = {NORTH: EAST, EAST: NORTH, SOUTH: WEST, WEST: SOUTH}[direction]
            next_cells.append((position + next_direction, next_direction))
        else:
            next_cells.append((position + direction, direction))
        return [item for item in next_cells if self.is_in_grid(item[0])]

    def is_in_grid(self,
                   position: Position) -> bool:
        return 0 <= position.row < self.height and 0 <= position.column < self.width

    def get_nb_energized_tiles(self) -> int:
        return sum(sum(len(cell) != 0 for cell in row) for row in self.visited_cells)


def compute_energized_tiles_number(lines: List[str]) -> int:
    contraption = Contraption(lines)
    contraption.propagate_beam()
    return contraption.get_nb_energized_tiles()
