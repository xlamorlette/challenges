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


NORTH: Final[Position] = Position(-1, 0)
EAST: Final[Position] = Position(0, 1)
SOUTH: Final[Position] = Position(1, 0)
WEST: Final[Position] = Position(0, -1)
ALL_DIRECTIONS: Final[list[Position]] = [NORTH, EAST, SOUTH, WEST]
