from typing import List


def compute_total_load(lines: List[str]) -> int:
    tilted_platform: List[str] = tilt_north(lines)
    return get_platform_load(tilted_platform)


def tilt_north(platform: List[str]) -> List[str]:
    columns: List[str] = list(map("".join, zip(*platform)))
    tilted_columns: List[str] = list(map(tilt_line, columns))
    return list(map("".join, zip(*tilted_columns)))


def tilt_line(line: str) -> str:
    groups: List[str] = line.split("#")
    return "#".join(map(stack_rocks_at_the_beginning, groups))


def stack_rocks_at_the_beginning(group: str) -> str:
    return "O" * group.count("O") + "." * group.count(".")


def get_platform_load(platform: List[str]) -> int:
    return sum(line.count("O") * (len(platform) - line_index) for line_index, line in enumerate(platform))
