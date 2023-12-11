from __future__ import annotations
import itertools
from dataclasses import dataclass
from typing import List


@dataclass
class Position:
    row: int
    column: int

    def __add__(self,
                other: Position) -> Position:
        return Position(self.row + other.row, self.column + other.column)

    def __repr__(self):
        return f"({self.row}, {self.column})"

    def manhattan_distance(self,
                           other: Position) -> int:
        return abs(self.row - other.row) + abs(self.column - other.column)


class Universe:
    galaxies: List[Position]

    def __init__(self,
                 lines: List[str]):
        lines = self.expand_empty_lines_and_rows(lines)
        self._detect_galaxies(lines)

    @staticmethod
    def expand_empty_lines_and_rows(lines: List[str]) -> List[str]:
        for column_index in reversed(range(len(lines[0]))):
            if sum(line[column_index] == "#" for line in lines) == 0:
                lines = [line[:column_index] + "." + line[column_index:] for line in lines]
        empty_line: str = "." * len(lines[0])
        for line_index in reversed(range(len(lines))):
            if lines[line_index].count("#") == 0:
                lines.insert(line_index, empty_line)
        return lines

    def _detect_galaxies(self,
                         lines: List[str]):
        self.galaxies = []
        for row, line in enumerate(lines):
            for column, character in enumerate(line):
                if character == "#":
                    self.galaxies.append(Position(row, column))

    def compute_sum_of_galaxy_pair_distance(self) -> int:
        return sum(galaxy_a.manhattan_distance(galaxy_b)
                   for galaxy_a, galaxy_b in itertools.combinations(self.galaxies, 2))


def compute_sum_of_pair_distances(lines: List[str]) -> int:
    universe = Universe(lines)
    return universe.compute_sum_of_galaxy_pair_distance()
