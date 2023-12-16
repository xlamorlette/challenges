from typing import Final, List

from src.day_16.the_floor_will_be_lava import Contraption, compute_energized_tiles_number
from src.util.position import Position, NORTH, SOUTH, EAST, WEST

INPUT: Final[str] = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")


def test_compute_energized_tiles_number():
    assert compute_energized_tiles_number(INPUT_LINES) == 46


def test_contraption_get_next_cells():
    contraption = Contraption(INPUT_LINES)
    assert contraption.get_next_cells(Position(0, 0), EAST) == [(Position(0, 1), EAST)]
    assert contraption.get_next_cells(Position(0, 0), SOUTH) == [(Position(1, 0), SOUTH)]
    assert contraption.get_next_cells(Position(0, 0), NORTH) == []
    assert contraption.get_next_cells(Position(0, 0), WEST) == []
    assert contraption.get_next_cells(Position(2, 5), WEST) == [(Position(1, 5), NORTH), (Position(3, 5), SOUTH)]
    assert contraption.get_next_cells(Position(1, 2), SOUTH) == [(Position(1, 3), EAST), (Position(1, 1), WEST)]
    assert contraption.get_next_cells(Position(0, 5), EAST) == [(Position(1, 5), SOUTH)]
    assert contraption.get_next_cells(Position(6, 4), SOUTH) == [(Position(6, 3), WEST)]


def test_contraption_propagate_beam():
    contraption = Contraption(INPUT_LINES)
    contraption.propagate_beam()
    assert contraption.visited_cells[0][0] == {EAST}
    assert contraption.visited_cells[0][2] == {WEST}
    assert contraption.visited_cells[7][1] == {SOUTH, NORTH}
