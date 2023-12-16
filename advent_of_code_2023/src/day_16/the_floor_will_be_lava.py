from dataclasses import dataclass
from typing import List, Set

from src.util.position import Position, NORTH, SOUTH, EAST, WEST


Direction = Position


@dataclass
class Beam:
    position: Position
    direction: Direction


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

    def get_nb_energized_tiles_by_propagation(self,
                                              beam: Beam = Beam(Position(0, 0), EAST)) -> int:
        self.propagate_beam(beam)
        return self.get_nb_energized_tiles()

    def propagate_beam(self,
                       start_beam: Beam = Beam(Position(0, 0), EAST)):
        self.visited_cells = [[set() for _column in range(self.width)] for _row in range(self.height)]
        self.visited_cells[start_beam.position.row][start_beam.position.column].add(start_beam.direction)
        propagation_list: List[Beam] = [start_beam]
        while len(propagation_list) > 0:
            next_beams: List[Beam] = self.get_next_beams(propagation_list.pop())
            for beam in next_beams:
                if beam.direction not in self.visited_cells[beam.position.row][beam.position.column]:
                    self.visited_cells[beam.position.row][beam.position.column].add(beam.direction)
                    propagation_list.append(beam)

    def get_next_beams(self,
                       beam: Beam) -> List[Beam]:
        next_beams: List[Beam] = []
        cell = self.grid[beam.position.row][beam.position.column]
        if cell == "-" and beam.direction in [NORTH, SOUTH]:
            next_beams.append(Beam(beam.position + EAST, EAST))
            next_beams.append(Beam(beam.position + WEST, WEST))
        elif cell == "|" and beam.direction in [WEST, EAST]:
            next_beams.append(Beam(beam.position + NORTH, NORTH))
            next_beams.append(Beam(beam.position + SOUTH, SOUTH))
        elif cell == "\\":
            next_direction = {NORTH: WEST, EAST: SOUTH, SOUTH: EAST, WEST: NORTH}[beam.direction]
            next_beams.append(Beam(beam.position + next_direction, next_direction))
        elif cell == "/":
            next_direction = {NORTH: EAST, EAST: NORTH, SOUTH: WEST, WEST: SOUTH}[beam.direction]
            next_beams.append(Beam(beam.position + next_direction, next_direction))
        else:
            next_beams.append(Beam(beam.position + beam.direction, beam.direction))
        return [beam for beam in next_beams if self.is_in_grid(beam.position)]

    def is_in_grid(self,
                   position: Position) -> bool:
        return 0 <= position.row < self.height and 0 <= position.column < self.width

    def get_nb_energized_tiles(self) -> int:
        return sum(sum(len(cell) != 0 for cell in row) for row in self.visited_cells)


def compute_energized_tiles_number(lines: List[str]) -> int:
    contraption = Contraption(lines)
    return contraption.get_nb_energized_tiles_by_propagation()


def compute_maximum_energized_tiles_number(lines: List[str]) -> int:
    contraption = Contraption(lines)
    beam_list: List[Beam] = \
        [Beam(Position(0, column), SOUTH) for column in range(contraption.width)] \
        + [Beam(Position(contraption.height - 1, column), NORTH) for column in range(contraption.width)] \
        + [Beam(Position(row, 0), EAST) for row in range(contraption.height)] \
        + [Beam(Position(row, contraption.width - 1), WEST) for row in range(contraption.height)]
    return max(contraption.get_nb_energized_tiles_by_propagation(beam) for beam in beam_list)
