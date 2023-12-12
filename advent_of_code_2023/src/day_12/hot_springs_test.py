from typing import Final, List

from src.day_12.hot_springs import compute_sum_of_broken_spring_arrangements, get_continuous_group_lengths, \
    get_nb_broken_arrangements, is_arrangement_valid

INPUT: Final[str] = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")


def test_compute_sum_of_broken_spring_arrangements():
    assert compute_sum_of_broken_spring_arrangements(INPUT_LINES) == 21


def test_get_nb_broken_arrangements():
    assert get_nb_broken_arrangements(INPUT_LINES[0]) == 1
    assert get_nb_broken_arrangements(INPUT_LINES[1]) == 4
    assert get_nb_broken_arrangements(INPUT_LINES[2]) == 1
    assert get_nb_broken_arrangements(INPUT_LINES[3]) == 1
    assert get_nb_broken_arrangements(INPUT_LINES[4]) == 4
    assert get_nb_broken_arrangements(INPUT_LINES[5]) == 10


def test_is_arrangement_valid():
    # ".??..??...?##."
    assert not is_arrangement_valid([11, 12], (1, 2, 5), [1, 1, 3])
    assert is_arrangement_valid([11, 12], (1, 5, 10), [1, 1, 3])


def test_get_continuous_group_lengths():
    assert not get_continuous_group_lengths([])
    assert get_continuous_group_lengths([11, 12, 1, 2, 5]) == [2, 1, 2]
