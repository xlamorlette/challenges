from typing import Final, List

from src.day_13.point_of_incidence import compute_sum_of_reflection_numbers, \
    compute_sum_of_smudged_reflection_numbers, get_horizontal_symmetry_axis, get_reflection_number, \
    get_smudged_reflection_number, get_vertical_symmetry_axis, is_horizontal_symmetry_axis

INPUT: Final[str] = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

INPUT_2: Final[str] = """##....###
.#.#.#.##
###..#...
##..####.
.##.#...#
#...#....
#...#....
.##.#...#
##..####.
###..#...
.###.#.##
##....###
##....###"""

INPUT_3: Final[str] = """#...###
.#.####
#..#...
.##.#..
.##.#..
#..#...
.#.####
#..####
#.##.##"""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")
PATTERN_1: Final[List[str]] = INPUT_LINES[:7]
PATTERN_2: Final[List[str]] = INPUT_LINES[8:]
PATTERN_3: Final[List[str]] = INPUT_2.split("\n")
PATTERN_4: Final[List[str]] = INPUT_3.split("\n")


def test_compute_sum_of_reflection_numbers():
    assert compute_sum_of_reflection_numbers(INPUT_LINES) == 405


def test_get_reflection_number():
    assert get_reflection_number(PATTERN_1) == 5
    assert get_reflection_number(PATTERN_2) == 400
    assert get_reflection_number(PATTERN_3) == 1200
    assert get_reflection_number(PATTERN_4) == 6


def test_get_vertical_symmetry_axis():
    assert get_vertical_symmetry_axis(PATTERN_1) == 5
    assert get_vertical_symmetry_axis(PATTERN_2) is None


def test_get_horizontal_symmetry_axis():
    assert get_horizontal_symmetry_axis(PATTERN_1) is None
    assert get_horizontal_symmetry_axis(PATTERN_2) == 4


def test_is_horizontal_symmetry_axis():
    assert not is_horizontal_symmetry_axis(PATTERN_2, 1)
    assert is_horizontal_symmetry_axis(PATTERN_2, 4)
    assert is_horizontal_symmetry_axis(PATTERN_3, 12)


def test_compute_sum_of_smudged_reflection_numbers():
    assert compute_sum_of_smudged_reflection_numbers(INPUT_LINES) == 400


def test_get_smudged_reflection_number():
    assert get_smudged_reflection_number(PATTERN_1) == 300
    assert get_smudged_reflection_number(PATTERN_2) == 100
