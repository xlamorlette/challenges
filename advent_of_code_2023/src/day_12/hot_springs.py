import itertools
from typing import List, Tuple


def compute_sum_of_broken_spring_arrangements(lines: List[str]) -> int:
    return sum(map(get_nb_broken_arrangements, lines))


def get_nb_broken_arrangements(line: str) -> int:
    spring_statuses, damaged_groups_string = line.split(" ")
    unknown_state_positions: List[int] = [index for index, character in enumerate(spring_statuses) if character == "?"]
    known_damaged_positions: List[int] = [index for index, character in enumerate(spring_statuses) if character == "#"]
    damaged_groups: List[int] = list(map(int, damaged_groups_string.split(",")))
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
    positions.sort()
    group_lengths: List[int] = []
    previous_position: int = -2
    current_group_length: int = 0
    for position in positions:
        if position == previous_position + 1:
            current_group_length += 1
        else:
            if current_group_length > 0:
                group_lengths.append(current_group_length)
            current_group_length = 1
        previous_position = position
    if current_group_length > 0:
        group_lengths.append(current_group_length)
    return group_lengths
