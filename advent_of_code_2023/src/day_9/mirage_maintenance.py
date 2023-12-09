from typing import List


def compute_extrapolated_values_sum(lines: List[str]) -> int:
    return sum(map(extrapolate_value, lines))


def extrapolate_value(line: str) -> int:
    sequence: List[int] = list(map(int, line.split()))
    sequences_list: List[List[int]] = get_difference_sequences(sequence)
    extrapolate_sequences(sequences_list)
    return sequences_list[0][-1]


def not_all_zeros(sequence: List[int]) -> bool:
    return any(value != 0 for value in sequence)


def get_differences(sequence: List[int]) -> List[int]:
    return [sequence[index + 1] - sequence[index] for index in range(len(sequence) - 1)]


def get_difference_sequences(sequence: List[int]) -> List[List[int]]:
    sequences_list: List[List[int]] = [sequence]
    while not_all_zeros(sequences_list[-1]):
        sequences_list.append(get_differences(sequences_list[-1]))
    return sequences_list


def extrapolate_sequences(sequences_list: List[List[int]]):
    for sequence_index in range(len(sequences_list) - 2, -1, -1):
        new_value: int = sequences_list[sequence_index][-1] + sequences_list[sequence_index + 1][-1]
        sequences_list[sequence_index].append(new_value)


def compute_extrapolated_previous_values_sum(lines: List[str]) -> int:
    return sum(map(extrapolate_previous_value, lines))


def extrapolate_previous_value(line: str) -> int:
    sequence: List[int] = list(map(int, line.split()))
    sequences_list: List[List[int]] = get_difference_sequences(sequence)
    extrapolate_sequences_backward(sequences_list)
    return sequences_list[0][0]


def extrapolate_sequences_backward(sequences_list: List[List[int]]):
    for sequence_index in range(len(sequences_list) - 2, -1, -1):
        new_value: int = sequences_list[sequence_index][0] - sequences_list[sequence_index + 1][0]
        sequences_list[sequence_index].insert(0, new_value)
