import itertools
from typing import List

from src.util.position import Position


class Universe:
    _empty_columns: List[int]
    _empty_rows: List[int]
    _expansion_factor: int
    _galaxies: List[Position]

    def __init__(self,
                 lines: List[str],
                 expansion_factor: int = 2):
        self._expansion_factor = expansion_factor
        self._empty_rows: List[int] = self.get_empty_rows(lines)
        self._empty_columns: List[int] = self.get_empty_columns(lines)
        self._galaxies = self.get_galaxies(lines)

    @staticmethod
    def get_empty_rows(lines: List[str]) -> List[int]:
        return [row_index for row_index, row in enumerate(lines) if "#" not in row]

    @classmethod
    def get_empty_columns(cls,
                          lines: List[str]) -> List[int]:
        return [column_index
                for column_index in range(len(lines[0])) if cls._is_column_empty(lines, column_index)]

    @staticmethod
    def _is_column_empty(lines: List[str],
                         column_index: int) -> bool:
        return all(line[column_index] != "#" for line in lines)

    @staticmethod
    def get_galaxies(lines: List[str]) -> List[Position]:
        return [Position(row, column)
                for row in range(len(lines)) for column in range(len(lines[0]))
                if lines[row][column] == "#"]

    def compute_sum_of_galaxy_pair_distance(self) -> int:
        return sum(self._get_distance(galaxy_a, galaxy_b)
                   for galaxy_a, galaxy_b in itertools.combinations(self._galaxies, 2))

    def _get_distance(self,
                      galaxy_a: Position,
                      galaxy_b: Position) -> int:
        return self._get_one_dimension_distance(galaxy_a.row, galaxy_b.row, self._empty_rows) \
               + self._get_one_dimension_distance(galaxy_a.column, galaxy_b.column, self._empty_columns)

    def _get_one_dimension_distance(self,
                                    position_a: int,
                                    position_b: int,
                                    empty_positions: List[int]) -> int:
        min_position = min(position_a, position_b)
        max_position = max(position_a, position_b)
        return sum(self._expansion_factor if position in empty_positions else 1
                   for position in range(min_position, max_position))


def compute_sum_of_pair_distances(lines: List[str],
                                  expansion_factor: int = 2) -> int:
    universe = Universe(lines, expansion_factor)
    return universe.compute_sum_of_galaxy_pair_distance()
