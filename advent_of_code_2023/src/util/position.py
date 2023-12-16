from __future__ import annotations
from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
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


NORTH: Final[Position] = Position(-1, 0)
EAST: Final[Position] = Position(0, 1)
SOUTH: Final[Position] = Position(1, 0)
WEST: Final[Position] = Position(0, -1)
