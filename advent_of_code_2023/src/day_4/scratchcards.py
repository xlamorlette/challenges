from typing import List, Set


def get_set_of_numbers(string_to_parse: str) -> Set[int]:
    return set(int(token) for token in string_to_parse.split(" ") if token != "")


def get_winning_numbers(card_str: str) -> Set[int]:
    winning_numbers_str = card_str.split(":")[1].split("|")[0]
    return get_set_of_numbers(winning_numbers_str)


def get_played_numbers(card_str: str) -> Set[int]:
    winning_numbers_str = card_str.split(":")[1].split("|")[1]
    return get_set_of_numbers(winning_numbers_str)


def compute_card_points(card_str: str) -> int:
    winning_numbers: Set[int] = get_winning_numbers(card_str)
    played_numbers: Set[int] = get_played_numbers(card_str)
    matching_numbers: Set[int] = winning_numbers.intersection(played_numbers)
    nb_matching_numbers = len(matching_numbers)
    if nb_matching_numbers == 0:
        return 0
    return pow(2, nb_matching_numbers - 1)


def compute_sum_of_points(card_lines: List[str]) -> int:
    return sum(compute_card_points(card_str) for card_str in card_lines)
