import itertools
from typing import List, Optional


def compute_sum_of_reflection_numbers(lines: List[str]) -> int:
    return sum(get_reflection_number(line) or 0 for line in get_patterns(lines))


def get_patterns(lines: List[str]) -> List[List[str]]:
    return [list(group)
            for line_is_empty, group in itertools.groupby(lines, lambda line: line == "")
            if not line_is_empty]


def get_reflection_number(lines: List[str],
                          target_differences_count: int = 0) -> int:
    if vertical_symmetry_axis := get_vertical_symmetry_axis(lines, target_differences_count):
        return vertical_symmetry_axis
    if horizontal_symmetry_axis := get_horizontal_symmetry_axis(lines, target_differences_count):
        return horizontal_symmetry_axis * 100
    assert False, "no reflection found"


def get_vertical_symmetry_axis(lines: List[str],
                               target_differences_count: int = 0) -> Optional[int]:
    columns: List[str] = list(map("".join, zip(*lines)))
    return get_horizontal_symmetry_axis(columns, target_differences_count)


def get_horizontal_symmetry_axis(lines: List[str],
                                 allowed_differences_count: int = 0) -> Optional[int]:
    for row in range(1, len(lines)):
        if is_horizontal_symmetry_axis(lines, row, allowed_differences_count):
            return row
    return None


def is_horizontal_symmetry_axis(lines: List[str],
                                row_axis: int,
                                target_differences_count: int = 0) -> bool:
    upper_part = list(reversed(lines[:row_axis]))
    lower_part = lines[row_axis:]
    differences = sum(sum(character_upper != character_lower
                          for character_upper, character_lower in zip(line_upper, line_lower))
                      for line_upper, line_lower in zip(upper_part, lower_part))
    return differences == target_differences_count


def compute_sum_of_smudged_reflection_numbers(lines: List[str]) -> int:
    return sum(map(get_smudged_reflection_number, get_patterns(lines)))


def get_smudged_reflection_number(lines: List[str]) -> int:
    return get_reflection_number(lines, 1)
