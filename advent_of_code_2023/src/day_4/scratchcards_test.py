from typing import Final, List

from src.day_4.scratchcards import compute_card_points, compute_sum_of_points, get_played_numbers, get_winning_numbers

CARD_LINES: Final[List[str]] = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
]


def test_compute_sum_of_points():
    assert compute_sum_of_points(CARD_LINES) == 13


def test_compute_card_points():
    assert compute_card_points(CARD_LINES[0]) == 8
    assert compute_card_points(CARD_LINES[1]) == 2
    assert compute_card_points(CARD_LINES[2]) == 2
    assert compute_card_points(CARD_LINES[3]) == 1
    assert compute_card_points(CARD_LINES[4]) == 0
    assert compute_card_points(CARD_LINES[5]) == 0


def test_get_winning_numbers():
    assert get_winning_numbers(CARD_LINES[0]) == {41, 48, 83, 86, 17}


def test_get_played_numbers():
    assert get_played_numbers(CARD_LINES[0]) == {83, 86, 6, 31, 17, 9, 48, 53}
