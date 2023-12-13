import itertools
from typing import List, Optional


def compute_sum_of_reflection_numbers(lines: List[str]) -> int:
    return sum(get_reflection_number(line) or 0 for line in get_patterns(lines))


def get_patterns(lines: List[str]) -> List[List[str]]:
    return [list(group)
            for line_is_empty, group in itertools.groupby(lines, lambda line: line == "")
            if not line_is_empty]


def get_reflection_number(lines: List[str],
                          excluded_vertical_axis: Optional[int] = None,
                          excluded_horizontal_axis: Optional[int] = None) -> Optional[int]:
    if vertical_symmetry_axis := get_vertical_symmetry_axis(lines, excluded_vertical_axis):
        return vertical_symmetry_axis
    if horizontal_symmetry_axis := get_horizontal_symmetry_axis(lines, excluded_horizontal_axis):
        return horizontal_symmetry_axis * 100
    return None


def get_vertical_symmetry_axis(lines: List[str],
                               excluded_axis: Optional[int] = None) -> Optional[int]:
    columns: List[str] = list(map("".join, zip(*lines)))
    return get_horizontal_symmetry_axis(columns, excluded_axis)


def get_horizontal_symmetry_axis(lines: List[str],
                                 excluded_axis: Optional[int] = None) -> Optional[int]:
    for row in range(1, len(lines)):
        if row == excluded_axis:
            continue
        if is_horizontal_symmetry_axis(lines, row):
            return row
    return None


def is_horizontal_symmetry_axis(lines: List[str],
                                row_axis: int) -> bool:
    upper_part = list(reversed(lines[:row_axis]))
    lower_part = lines[row_axis:]
    upper_part = upper_part[:len(lower_part)]
    lower_part = lower_part[:len(upper_part)]
    return upper_part == lower_part


def compute_sum_of_smudged_reflection_numbers(lines: List[str]) -> int:
    return sum(map(get_smudged_reflection_number, get_patterns(lines)))


def get_smudged_reflection_number(lines: List[str]) -> int:
    reflection_number = get_reflection_number(lines) or 0
    excluded_vertical_axis: Optional[int] = reflection_number if reflection_number < 100 else None
    excluded_horizontal_axis: Optional[int] = int(reflection_number / 100) if reflection_number >= 100 else None
    for row, line in enumerate(lines):
        for column in range(len(lines[0])):
            fixed_line = line[:column] + inverted_character(line[column]) + line[column + 1:]
            fixed_lines = lines[:row] + [fixed_line] + lines[row + 1:]
            if smudged_reflection_number := get_reflection_number(fixed_lines, excluded_vertical_axis,
                                                                  excluded_horizontal_axis):
                return smudged_reflection_number
    return 0


def inverted_character(character: str) -> str:
    return "." if character == "#" else "#"
