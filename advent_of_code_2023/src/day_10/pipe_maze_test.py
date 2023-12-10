from typing import Final, List

from src.day_10.pipe_maze import Position, Sketch, compute_farthest_distance, EAST, NORTH, SOUTH, WEST

INPUT_1: Final[str] = """.....
.S-7.
.|.|.
.L-J.
....."""

INPUT_2: Final[str] = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

INPUT_1_LINES: Final[List[str]] = INPUT_1.split("\n")
INPUT_2_LINES: Final[List[str]] = INPUT_2.split("\n")


def test_compute_farthest_distance():
    assert compute_farthest_distance(INPUT_1_LINES) == 4
    assert compute_farthest_distance(INPUT_2_LINES) == 8


def test_position_add():
    assert Position(5, 5) + NORTH == Position(4, 5)
    assert Position(5, 5) + EAST == Position(5, 6)
    assert Position(5, 5) + SOUTH == Position(6, 5)
    assert Position(5, 5) + WEST == Position(5, 4)


def test_sketch_get_starting_position():
    assert Sketch(INPUT_1_LINES).get_starting_position() == Position(1, 1)
    assert Sketch(INPUT_2_LINES).get_starting_position() == Position(2, 0)


def test_sketch_get_a_starting_direction():
    assert Sketch(INPUT_1_LINES).get_a_starting_direction(Position(1, 1)) in [EAST, SOUTH]
    assert Sketch(INPUT_2_LINES).get_a_starting_direction(Position(2, 0)) in [EAST, SOUTH]


def test_sketch_get_next_direction():
    sketch = Sketch(INPUT_1_LINES)
    assert sketch.get_next_direction(Position(1, 2), EAST) == EAST
    assert sketch.get_next_direction(Position(1, 3), EAST) == SOUTH


def test_sketch_get_main_loop_length():
    assert Sketch(INPUT_1_LINES).get_main_loop_length() == 8
    assert Sketch(INPUT_2_LINES).get_main_loop_length() == 16
