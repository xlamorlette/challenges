import itertools
from typing import List, Optional


def compute_sum_of_reflection_numbers(lines: List[str]) -> int:
    return sum(map(get_reflection_number, get_patterns(lines)))


def get_patterns(lines: List[str]) -> List[List[str]]:
    return [list(group)
            for line_is_empty, group in itertools.groupby(lines, lambda line: line == "")
            if not line_is_empty]


def get_reflection_number(lines: List[str],
                          excluded_vertical_axis: Optional[int] = None,
                          excluded_horizontal_axis: Optional[int] = None) -> int:
    vertical_symmetry_axis: Optional[int] = get_vertical_symmetry_axis(lines, excluded_vertical_axis)
    if vertical_symmetry_axis:
        return vertical_symmetry_axis
    horizontal_symmetry_axis: Optional[int] = get_horizontal_symmetry_axis(lines, excluded_horizontal_axis)
    if horizontal_symmetry_axis:
        return horizontal_symmetry_axis * 100
    return 0


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
    symmetric_size = min(row_axis, len(lines) - row_axis)
    upper_part: List[str] = lines[row_axis - symmetric_size: row_axis]
    lower_part: List[str] = lines[row_axis: row_axis + symmetric_size]
    return upper_part == list(reversed(lower_part))


def compute_sum_of_smudged_reflection_numbers(lines: List[str]) -> int:
    return sum(map(get_smudged_reflection_number, get_patterns(lines)))


def get_smudged_reflection_number(lines: List[str]) -> int:
    reflection_number = get_reflection_number(lines)
    excluded_vertical_axis: Optional[int] = reflection_number if reflection_number < 100 else None
    excluded_horizontal_axis: Optional[int] = int(reflection_number / 100) if reflection_number >= 100 else None
    for row, line in enumerate(lines):
        for column in range(len(lines[0])):
            fixed_line = line[:column] + inverted_character(line[column]) + line[column + 1:]
            fixed_lines = lines[:row] + [fixed_line] + lines[row + 1:]
            smudged_reflection_number = get_reflection_number(fixed_lines, excluded_vertical_axis,
                                                              excluded_horizontal_axis)
            if smudged_reflection_number != 0:
                return smudged_reflection_number
    return 0


def inverted_character(character: str) -> str:
    return "." if character == "#" else "#"
