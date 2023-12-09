from itertools import pairwise
from typing import List


def compute_extrapolated_values_sum(lines: List[str]) -> int:
    return sum(map(extrapolate_value_from_line, lines))


def extrapolate_value_from_line(line: str) -> int:
    sequence: List[int] = list(map(int, line.split()))
    return extrapolate_value_from_list(sequence)


def extrapolate_value_from_list(sequence: List[int]) -> int:
    sequences_list: List[List[int]] = get_difference_sequences(sequence)
    extrapolate_sequences(sequences_list)
    return sequences_list[0][-1]


def get_difference_sequences(sequence: List[int]) -> List[List[int]]:
    sequences_list: List[List[int]] = [sequence]
    while not_all_zeros(sequences_list[-1]):
        sequences_list.append(get_differences(sequences_list[-1]))
    return sequences_list


def not_all_zeros(sequence: List[int]) -> bool:
    return any(value != 0 for value in sequence)


def get_differences(sequence: List[int]) -> List[int]:
    return [next_value - value for value, next_value in pairwise(sequence)]


def extrapolate_sequences(sequences_list: List[List[int]]):
    for sequence_index in range(len(sequences_list) - 2, -1, -1):
        new_value: int = sequences_list[sequence_index][-1] + sequences_list[sequence_index + 1][-1]
        sequences_list[sequence_index].append(new_value)


def compute_extrapolated_previous_values_sum(lines: List[str]) -> int:
    return sum(map(extrapolate_previous_value, lines))


def extrapolate_previous_value(line: str) -> int:
    sequence: List[int] = list(map(int, line.split()))
    reversed_sequence = list(reversed(sequence))
    return extrapolate_value_from_list(reversed_sequence)
