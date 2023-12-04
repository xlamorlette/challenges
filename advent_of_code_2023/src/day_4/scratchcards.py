from typing import List, Set


def compute_sum_of_points(card_lines: List[str]) -> int:
    return sum(compute_card_points(card_str) for card_str in card_lines)


def compute_card_points(card_str: str) -> int:
    nb_matching_numbers = compute_nb_matching_numbers(card_str)
    if nb_matching_numbers == 0:
        return 0
    return pow(2, nb_matching_numbers - 1)


def compute_nb_matching_numbers(card_str):
    winning_numbers: Set[int] = get_winning_numbers(card_str)
    played_numbers: Set[int] = get_played_numbers(card_str)
    matching_numbers: Set[int] = winning_numbers.intersection(played_numbers)
    return len(matching_numbers)


def get_winning_numbers(card_str: str) -> Set[int]:
    winning_numbers_str = card_str.split(":")[1].split("|")[0]
    return get_set_of_numbers(winning_numbers_str)


def get_played_numbers(card_str: str) -> Set[int]:
    winning_numbers_str = card_str.split(":")[1].split("|")[1]
    return get_set_of_numbers(winning_numbers_str)


def get_set_of_numbers(string_to_parse: str) -> Set[int]:
    return set(int(token) for token in string_to_parse.split(" ") if token != "")


def compute_nb_cards(card_lines: List[str]) -> int:
    nb_matching_numbers_per_card: List[int] = get_nb_matching_numbers_per_card(card_lines)
    nb_copies_won_per_card: List[int] = get_nb_copies_won_per_card(nb_matching_numbers_per_card)
    return sum(nb_copies_won_per_card) + len(nb_copies_won_per_card)


def get_nb_matching_numbers_per_card(card_lines: List[str]) -> List[int]:
    return [compute_nb_matching_numbers(card) for card in card_lines]


def get_nb_copies_won_per_card(nb_matching_numbers_per_card: List[int]) -> List[int]:
    nb_copies_won_per_card: List[int] = []
    for nb_matching_numbers in reversed(nb_matching_numbers_per_card):
        nb_copies_won = nb_matching_numbers + sum(nb_copies_won_per_card[:nb_matching_numbers + 1])
        nb_copies_won_per_card.insert(0, nb_copies_won)
    return nb_copies_won_per_card
