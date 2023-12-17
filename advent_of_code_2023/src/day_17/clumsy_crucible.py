from dataclasses import dataclass
from heapq import heappop, heappush

from src.util.position import Position, ALL_DIRECTIONS, EAST, SOUTH


@dataclass(frozen=True, order=True)
class LocalPath:
    position: Position
    direction: Position
    length: int


class City:
    grid: dict[Position, int]
    nb_cols: int
    nb_rows: int
    visited_path: set[LocalPath]
    minimum_length: int
    maximum_length: int

    def __init__(self,
                 lines: list[str],
                 minimum_length: int = 0,
                 maximum_length: int = 3):
        self.nb_rows = len(lines)
        self.nb_cols = len(lines[0])
        self.minimum_length = minimum_length
        self.maximum_length = maximum_length
        self.grid = {Position(row, column): int(char)
                     for row, line in enumerate(lines) for column, char in enumerate(line)}

    def get_least_heat_loss(self) -> int:
        start_position = Position(0, 0)
        target_position = Position(self.nb_rows - 1, self.nb_cols - 1)
        self.visited_path = set()
        propagation_heap = [
            (0, LocalPath(start_position, EAST, 0)),
            (0, LocalPath(start_position, SOUTH, 0))
        ]
        while propagation_heap:
            loss, path = heappop(propagation_heap)
            if path.position == target_position:
                if path.length < self.minimum_length:
                    continue
                return loss
            if path in self.visited_path:
                continue
            self.visited_path.add(path)
            for next_path in self.get_next_paths(path):
                if next_path.position in self.grid:
                    next_loss = loss + self.grid[next_path.position]
                    heappush(propagation_heap, (next_loss, next_path))
        assert False, "target position not reached"

    def get_next_paths(self,
                       path: LocalPath) -> list[LocalPath]:
        next_paths: list[LocalPath] = []
        if path.length < self.maximum_length:
            next_paths.append(LocalPath(path.position + path.direction, path.direction, path.length + 1))
        if path.length >= self.minimum_length:
            new_directions: list[Position] = [direction for direction in ALL_DIRECTIONS
                                              if direction not in [path.direction, path.direction.opposite()]]
            next_paths += [LocalPath(path.position + direction, direction, 1) for direction in new_directions]
        return next_paths


def compute_least_heat_loss(lines: list[str]) -> int:
    return City(lines).get_least_heat_loss()


def compute_least_heat_loss_ultra(lines: list[str]) -> int:
    return City(lines, 4, 10).get_least_heat_loss()
