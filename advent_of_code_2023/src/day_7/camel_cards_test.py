from typing import Final, List

from src.day_7.camel_cards import Hand, HandType, compute_total_winnings, get_card_value

INPUT: Final[str] = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")


def test_compute_total_winnings():
    assert compute_total_winnings(INPUT_LINES) == 5905


def test_hand_init():
    hand = Hand("32T3K 765")
    assert hand.cards == "32T3K"
    assert hand.bid == 765


def test_hand_compute_type():
    assert Hand("23456 1").type == HandType.HIGH_CARD
    assert Hand("32T3K 1").type == HandType.ONE_PAIR
    assert Hand("KK677 1").type == HandType.TWO_PAIRS
    assert Hand("T5535 1").type == HandType.THREE_OF_KIND
    assert Hand("Q3QQ3 1").type == HandType.FULL_HOUSE
    assert Hand("32222 1").type == HandType.FOUR_OF_A_KIND
    assert Hand("22222 1").type == HandType.FIVE_OF_A_KIND


def test_hand_compute_type_with_jokers():
    assert Hand("23J56 1").type == HandType.ONE_PAIR
    assert Hand("22J56 1").type == HandType.THREE_OF_KIND
    assert Hand("22J33 1").type == HandType.FULL_HOUSE
    assert Hand("22J23 1").type == HandType.FOUR_OF_A_KIND
    assert Hand("22J22 1").type == HandType.FIVE_OF_A_KIND
    assert Hand("2JJ56 1").type == HandType.THREE_OF_KIND
    assert Hand("2JJ26 1").type == HandType.FOUR_OF_A_KIND
    assert Hand("2JJ22 1").type == HandType.FIVE_OF_A_KIND
    assert Hand("2JJJ6 1").type == HandType.FOUR_OF_A_KIND
    assert Hand("2JJ2J 1").type == HandType.FIVE_OF_A_KIND
    assert Hand("2JJJJ 1").type == HandType.FIVE_OF_A_KIND
    assert Hand("JJJJJ 1").type == HandType.FIVE_OF_A_KIND


def test_hand_compute_value():
    assert Hand("32T3K 1").value == 20302100312
    assert Hand("23456 1").value == 10203040506
    assert Hand("KK677 1").value == 31212060707
    assert Hand("Q5535 1").value == 41105050305
    assert Hand("QAQQA 1").value == 51113111113
    assert Hand("32222 1").value == 60302020202
    assert Hand("22222 1").value == 70202020202


def test_get_card_value():
    assert get_card_value("J") == 1
    assert get_card_value("2") == 2
    assert get_card_value("T") == 10
    assert get_card_value("A") == 13
