from typing import Final, List

from src.day_11.cosmic_expansion import Universe, Position, compute_sum_of_pair_distances

INPUT: Final[str] = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")


def test_compute_sum_of_pair_distances():
    assert compute_sum_of_pair_distances(INPUT_LINES) == 374


def test_universe_get_empty_rows():
    assert Universe.get_empty_rows(INPUT_LINES) == [3, 7]


def test_universe_get_empty_columns():
    assert Universe.get_empty_columns(INPUT_LINES) == [2, 5, 8]


def test_universe_get_galaxies():
    assert Universe.get_galaxies(INPUT_LINES) == [
        Position(0, 3),
        Position(1, 7),
        Position(2, 0),
        Position(4, 6),
        Position(5, 1),
        Position(6, 9),
        Position(8, 7),
        Position(9, 0),
        Position(9, 4)
    ]


def test_compute_sum_of_pair_distances_with_expansion_factor():
    assert compute_sum_of_pair_distances(INPUT_LINES, 10) == 1030
    assert compute_sum_of_pair_distances(INPUT_LINES, 100) == 8410
