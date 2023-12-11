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


def test_universe_init():
    universe = Universe(INPUT_LINES)
    assert universe.galaxies == [
        Position(0, 4),
        Position(1, 9),
        Position(2, 0),
        Position(5, 8),
        Position(6, 1),
        Position(7, 12),
        Position(10, 9),
        Position(11, 0),
        Position(11, 5)
    ]


def test_universe_expand_empty_lines_and_rows():
    assert Universe.expand_empty_lines_and_rows(INPUT_LINES) == [
        "....#........",
        ".........#...",
        "#............",
        ".............",
        ".............",
        "........#....",
        ".#...........",
        "............#",
        ".............",
        ".............",
        ".........#...",
        "#....#......."
    ]
