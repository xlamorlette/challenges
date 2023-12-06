from typing import Final, List

from src.day_6.boat_race import compute_distance, compute_number_of_ways_to_win, compute_number_of_ways_to_win_2, \
    compute_number_of_ways_to_win_race

INPUT: Final[str] = """Time:      7  15   30
Distance:  9  40  200
"""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")


def test_compute_number_of_ways_to_win():
    assert compute_number_of_ways_to_win(INPUT_LINES) == 288


def test_compute_number_of_ways_to_win_race():
    assert compute_number_of_ways_to_win_race(7, 9) == 4
    assert compute_number_of_ways_to_win_race(15, 40) == 8
    assert compute_number_of_ways_to_win_race(30, 200) == 9


def test_compute_distance():
    assert compute_distance(0, 7) == 0
    assert compute_distance(1, 7) == 6
    assert compute_distance(2, 7) == 10
    assert compute_distance(3, 7) == 12
    assert compute_distance(4, 7) == 12
    assert compute_distance(5, 7) == 10
    assert compute_distance(6, 7) == 6
    assert compute_distance(7, 7) == 0


def test_compute_number_of_ways_to_win_2():
    assert compute_number_of_ways_to_win_2(INPUT_LINES) == 71503
