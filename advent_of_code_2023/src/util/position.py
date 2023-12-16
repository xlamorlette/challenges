from __future__ import annotations
from dataclasses import dataclass
from typing import Final


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

    def __key(self):
        return self.row, self.column

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.__key() == other.__key()  # pylint: disable=protected-access
        return NotImplemented


NORTH: Final[Position] = Position(-1, 0)
EAST: Final[Position] = Position(0, 1)
SOUTH: Final[Position] = Position(1, 0)
WEST: Final[Position] = Position(0, -1)
