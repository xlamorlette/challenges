from typing import Final, List

from src.day_9.mirage_maintenance import compute_extrapolated_previous_values_sum, compute_extrapolated_values_sum, \
    extrapolate_previous_value, extrapolate_value, get_differences, not_all_zeros

INPUT: Final[str] = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")


def test_compute_extrapolated_values_sum():
    assert compute_extrapolated_values_sum(INPUT_LINES) == 114


def test_extrapolate_value():
    assert extrapolate_value(INPUT_LINES[0]) == 18
    assert extrapolate_value(INPUT_LINES[1]) == 28
    assert extrapolate_value(INPUT_LINES[2]) == 68


def test_not_all_zeros():
    assert not_all_zeros([0, 1])
    assert not not_all_zeros([0, 0])
    assert not not_all_zeros([])


def test_get_differences():
    assert get_differences([0, 3, 6, 9, 12, 15]) == [3, 3, 3, 3, 3]
    assert get_differences([3, 3, 3, 3, 3]) == [0, 0, 0, 0]
    assert get_differences([1, 3, 6, 10, 15, 21]) == [2, 3, 4, 5, 6]


def test_compute_extrapolated_previous_values_sum():
    assert compute_extrapolated_previous_values_sum(INPUT_LINES) == 2


def test_extrapolate_previous_value():
    assert extrapolate_previous_value(INPUT_LINES[0]) == -3
    assert extrapolate_previous_value(INPUT_LINES[1]) == 0
    assert extrapolate_previous_value(INPUT_LINES[2]) == 5
