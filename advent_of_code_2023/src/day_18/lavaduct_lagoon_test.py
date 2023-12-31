from typing import Final

from src.day_18.lavaduct_lagoon import compute_lagoon_capacity, compute_lagoon_capacity_triangle_formula, \
    get_direction_and_length

INPUT: Final[str] = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

INPUT_LINES: Final[list[str]] = INPUT.split("\n")


def test_compute_lagoon_capacity():
    assert compute_lagoon_capacity(INPUT_LINES) == 62


def test_compute_lagoon_capacity_triangle_formula():
    assert compute_lagoon_capacity_triangle_formula(INPUT_LINES) == 62


def test_compute_lagoon_capacity_second_part():
    assert compute_lagoon_capacity_triangle_formula(INPUT_LINES, second_part=True) == 952408144115


def test_get_direction_and_length():
    assert get_direction_and_length(INPUT_LINES[0]) == ("R", 6)
    assert get_direction_and_length(INPUT_LINES[0], second_part=True) == ("R", 461937)
