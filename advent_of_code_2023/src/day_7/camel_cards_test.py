from typing import Final, List

from src.day_7.camel_cards import Hand, HandType, compute_total_winnings

INPUT: Final[str] = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")


def test_compute_total_winnings():
    assert compute_total_winnings(INPUT_LINES) == 6440


def test_hand_init():
    hand = Hand("32T3K 765")
    assert hand.cards == "32T3K"
    assert hand.bid == 765


def test_hand_determine_type():
    assert Hand("23456 765").type == HandType.HIGH_CARD
    assert Hand("32T3K 765").type == HandType.ONE_PAIR
    assert Hand("KK677 28").type == HandType.TWO_PAIRS
    assert Hand("T55J5 684").type == HandType.THREE_OF_KIND
    assert Hand("QJQQJ 1").type == HandType.FULL_HOUSE
    assert Hand("32222 1").type == HandType.FOUR_OF_A_KIND
    assert Hand("22222 1").type == HandType.FIVE_OF_A_KIND


def test_hand_compute_value():
    assert Hand("32T3K 1").value == 20302100313
    assert Hand("23456 1").value == 10203040506
    assert Hand("KK677 1").value == 31313060707
    assert Hand("Q55J5 1").value == 41205051105
    assert Hand("QAQQA 1").value == 51214121214
    assert Hand("32222 1").value == 60302020202
    assert Hand("22222 1").value == 70202020202
