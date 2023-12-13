import itertools
from typing import List, Optional


def compute_sum_of_reflection_numbers(lines: List[str]) -> int:
    patterns: List[List[str]] = [list(group)
                                 for line_is_empty, group in itertools.groupby(lines, lambda line: line == "")
                                 if not line_is_empty]
    return sum(map(get_reflection_number, patterns))


def get_reflection_number(lines: List[str]) -> int:
    vertical_symmetry_axis: Optional[int] = get_vertical_symmetry_axis(lines)
    if vertical_symmetry_axis:
        return vertical_symmetry_axis
    horizontal_symmetry_axis: Optional[int] = get_horizontal_symmetry_axis(lines)
    if horizontal_symmetry_axis:
        return horizontal_symmetry_axis * 100
    assert False, f"no symmetry found for {lines}"


def get_vertical_symmetry_axis(lines: List[str]) -> Optional[int]:
    columns: List[str] = list(map("".join, zip(*lines)))
    return get_horizontal_symmetry_axis(columns)


def get_horizontal_symmetry_axis(lines: List[str]) -> Optional[int]:
    for row in range(1, len(lines)):
        if is_horizontal_symmetry_axis(lines, row):
            return row
    return None


def is_horizontal_symmetry_axis(lines: List[str],
                                row_axis: int) -> bool:
    symmetric_size = min(row_axis, len(lines) - row_axis)
    upper_part: List[str] = lines[row_axis - symmetric_size: row_axis]
    lower_part: List[str] = lines[row_axis: row_axis + symmetric_size]
    return upper_part == list(reversed(lower_part))
