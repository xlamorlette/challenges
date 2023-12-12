import itertools
from typing import List, Tuple


def compute_sum_of_broken_spring_arrangements(lines: List[str]) -> int:
    return sum(map(get_nb_broken_arrangements, lines))


def get_nb_broken_arrangements(line: str) -> int:
    statuses, damaged_groups_string = line.split(" ")
    damaged_groups: List[int] = list(map(int, damaged_groups_string.split(",")))
    unknown_state_positions: List[int] = [index for index, character in enumerate(statuses) if character == "?"]
    known_damaged_positions: List[int] = [index for index, character in enumerate(statuses) if character == "#"]
    nb_damaged: int = sum(damaged_groups)
    nb_unknown_damaged: int = nb_damaged - len(known_damaged_positions)
    return sum(is_arrangement_valid(known_damaged_positions, candidate_damaged_positions, damaged_groups)
               for candidate_damaged_positions in itertools.combinations(unknown_state_positions,
                                                                         nb_unknown_damaged))


def is_arrangement_valid(known_damaged_positions: List[int],
                         candidate_damaged_positions: Tuple,
                         damaged_groups: List[int]) -> bool:
    damaged_positions: List[int] = known_damaged_positions + list(candidate_damaged_positions)
    return get_continuous_group_lengths(damaged_positions) == damaged_groups


def get_continuous_group_lengths(positions: List[int]) -> List[int]:
    length: int = max(positions) + 1
    string_representation: str = "".join("#" if index in positions else " " for index in range(length))
    return [len(group) for group in string_representation.split()]


def compute_sum_of_broken_spring_arrangements_unfolded(lines: List[str]) -> int:
    return sum(map(get_nb_broken_arrangements_unfolded, lines))


def get_nb_broken_arrangements_unfolded(line: str) -> int:
    spring_statuses, damaged_groups_string = line.split(" ")
    expanded_spring_statuses: str = "?".join([spring_statuses] * 5)
    expanded_damaged_groups_string: str = ",".join([damaged_groups_string] * 5)
    expanded_line: str = expanded_spring_statuses + " " + expanded_damaged_groups_string
    return get_nb_broken_arrangements(expanded_line)
