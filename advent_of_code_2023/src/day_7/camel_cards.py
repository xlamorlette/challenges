from collections import Counter
from enum import IntEnum
from typing import Final, List


class HandType(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_KIND = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


CARDS_BY_INCREASING_VALUE: Final[str] = "J23456789TQKA"


def get_card_value(card: str) -> int:
    return CARDS_BY_INCREASING_VALUE.index(card) + 1


class Hand:
    bid: int
    cards: str
    type: HandType
    value: int

    def __init__(self,
                 line: str):
        line_items = line.split()
        self.cards = line_items[0]
        self.bid = int(line_items[1])
        self.type = self._compute_type(self.cards)
        self._compute_value()

    @staticmethod
    def _compute_type(cards: str) -> HandType:
        number_of_jokers = cards.count("J")
        if number_of_jokers == 5:
            return HandType.FIVE_OF_A_KIND
        cards_without_jokers = list(filter(lambda card: card != "J", cards))
        number_per_card_in_hand = Counter(cards_without_jokers)
        card_cardinals = sorted(list(number_per_card_in_hand.values()), reverse=True)
        # the jokers add up to the most frequent card
        card_cardinals[0] += number_of_jokers
        match card_cardinals[0]:
            case 5:
                return HandType.FIVE_OF_A_KIND
            case 4:
                return HandType.FOUR_OF_A_KIND
            case 3:
                if card_cardinals[1] == 2:
                    return HandType.FULL_HOUSE
                return HandType.THREE_OF_KIND
            case 2:
                if card_cardinals[1] == 2:
                    return HandType.TWO_PAIRS
                return HandType.ONE_PAIR
            case _other:
                return HandType.HIGH_CARD

    def _compute_value(self):
        value_string: str = str(int(self.type))
        for card in self.cards:
            value_string += f"{get_card_value(card):02d}"
        self.value = int(value_string)

    def __repr__(self):
        return f"({self.cards}, {self.bid}, {self.value})"


def compute_total_winnings(lines: List[str]) -> int:
    hands: List[Hand] = [Hand(line) for line in lines]
    hands.sort(key=lambda hand: hand.value)
    return sum(hand.bid * (rank + 1) for rank, hand in enumerate(hands))
