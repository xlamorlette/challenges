import functools
from typing import List, Tuple


def compute_sum_of_broken_spring_arrangements(lines: List[str]) -> int:
    return sum(map(get_nb_broken_arrangements, lines))


def get_nb_broken_arrangements(line: str) -> int:
    statuses, damaged_groups_string = line.split(" ")
    damaged_groups: Tuple = tuple(map(int, damaged_groups_string.split(",")))
    return get_nb_combinations(statuses, damaged_groups)


@functools.cache
def get_nb_combinations(statuses: str,
                        damaged_groups: Tuple) -> int:
    if len(damaged_groups) == 0:
        return int("#" not in statuses)
    if len(statuses) == 0:
        return int(len(damaged_groups) == 0)
    match statuses[0]:
        case ".":
            return get_nb_combinations(statuses[1:], damaged_groups)
        case "?":
            alternate_statuses = ["#" + statuses[1:], "." + statuses[1:]]
            return sum(get_nb_combinations(alternate, damaged_groups) for alternate in alternate_statuses)
        case "#":
            return get_nb_combinations_matching_first_group(statuses, damaged_groups)
        case other:
            assert False, f"invalid character in statuses: {other}"


def get_nb_combinations_matching_first_group(statuses: str,
                                             damaged_groups: Tuple) -> int:
    assert statuses[0] == "#", f"unexpected statuses when matching first group: {statuses}"
    group_length: int = damaged_groups[0]
    if len(statuses) < group_length:
        return 0
    if "." in statuses[:group_length]:
        return 0
    if len(statuses) > group_length and statuses[group_length] == "#":
        return 0
    return get_nb_combinations(statuses[group_length + 1:], damaged_groups[1:])


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
