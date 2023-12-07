from collections import Counter
from enum import IntEnum
from typing import Dict, Final, List


class HandType(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_KIND = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


VALUE_PER_CARD: Final[Dict[str, int]] = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}


class Hand:
    bid: int
    cards: List[str]
    type: HandType
    value: int

    def __init__(self,
                 line: str):
        line_items = line.split()
        self.cards = list(line_items[0])
        self.bid = int(line_items[1])
        self._determine_type()
        self._compute_value()

    def _determine_type(self):
        number_per_card_in_hand = Counter(self.cards)
        card_cardinals = list(number_per_card_in_hand.values())
        card_cardinals.sort(reverse=True)
        if card_cardinals[0] == 5:
            self.type = HandType.FIVE_OF_A_KIND
        elif card_cardinals[0] == 4:
            self.type = HandType.FOUR_OF_A_KIND
        elif card_cardinals[0] == 3 and card_cardinals[1] == 2:
            self.type = HandType.FULL_HOUSE
        elif card_cardinals[0] == 3:
            self.type = HandType.THREE_OF_KIND
        elif card_cardinals[0] == 2 and card_cardinals[1] == 2:
            self.type = HandType.TWO_PAIRS
        elif card_cardinals[0] == 2:
            self.type = HandType.ONE_PAIR
        else:
            self.type = HandType.HIGH_CARD

    def _compute_value(self):
        value_string: str = str(int(self.type))
        for card in self.cards:
            value_string += f"{VALUE_PER_CARD[card]:02d}"
        self.value = int(value_string)

    def __repr__(self):
        return f"({''.join(self.cards)}, {self.bid}, {self.value})"


def compute_total_winnings(lines: List[str]) -> int:
    hands: List[Hand] = [Hand(line) for line in lines]
    hands.sort(key=lambda hand: hand.value)
    return sum(hand.bid * (rank + 1) for rank, hand in enumerate(hands))
