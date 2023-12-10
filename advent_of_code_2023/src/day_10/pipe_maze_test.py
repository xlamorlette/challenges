from typing import Final, List

from src.day_10.pipe_maze import Position, Sketch, EAST, NORTH, SOUTH, WEST, compute_farthest_distance, \
    get_nb_enclosed_tiles

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


INPUT_3: Final[str] = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

INPUT_4: Final[str] = """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
.........."""

INPUT_5: Final[str] = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

INPUT_6: Final[str] = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

INPUT_3_LINES: Final[List[str]] = INPUT_3.split("\n")
INPUT_4_LINES: Final[List[str]] = INPUT_4.split("\n")
INPUT_5_LINES: Final[List[str]] = INPUT_5.split("\n")
INPUT_6_LINES: Final[List[str]] = INPUT_6.split("\n")


def test_get_nb_enclosed_tiles():
    assert get_nb_enclosed_tiles(INPUT_1_LINES) == 1
    assert get_nb_enclosed_tiles(INPUT_2_LINES) == 1
    assert get_nb_enclosed_tiles(INPUT_3_LINES) == 4
    assert get_nb_enclosed_tiles(INPUT_4_LINES) == 4
    assert get_nb_enclosed_tiles(INPUT_5_LINES) == 8
    assert get_nb_enclosed_tiles(INPUT_6_LINES) == 10
