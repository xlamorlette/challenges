from typing import Dict, List, Tuple


def compute_total_load(lines: List[str]) -> int:
    tilted_platform: List[str] = tilt_north(lines)
    return get_platform_load(tilted_platform)


def tilt_north(platform: List[str]) -> List[str]:
    columns: List[str] = list(map("".join, zip(*platform)))
    tilted_columns: List[str] = list(map(tilt_line, columns))
    return list(map("".join, zip(*tilted_columns)))


def tilt_south(platform: List[str]) -> List[str]:
    reversed_columns: List[str] = ["".join(column)[::-1] for column in zip(*platform)]
    tilted_columns: List[str] = ["".join(tilt_line(column)[::-1]) for column in reversed_columns]
    return list(map("".join, zip(*tilted_columns)))


def tilt_east(platform: List[str]) -> List[str]:
    reversed_lines: List[str] = ["".join(line)[::-1] for line in platform]
    return ["".join(tilt_line(line))[::-1] for line in reversed_lines]


def tilt_west(platform: List[str]) -> List[str]:
    return list(map(tilt_line, platform))


def tilt_line(line: str) -> str:
    groups: List[str] = line.split("#")
    return "#".join(map(stack_rocks_at_the_beginning, groups))


def stack_rocks_at_the_beginning(group: str) -> str:
    return "O" * group.count("O") + "." * group.count(".")


def get_platform_load(platform: List[str]) -> int:
    return sum(line.count("O") * (len(platform) - line_index) for line_index, line in enumerate(platform))


def compute_one_billion_spins_load(lines: List[str]) -> int:
    cycle_start, cycle_end = get_spin_cycle(lines)
    nb_spin = ((10 ** 9 - cycle_start) % (cycle_end - cycle_start)) + cycle_start
    for _spin_index in range(nb_spin):
        lines = spin(lines)
    return get_platform_load(lines)


def get_spin_cycle(platform: List[str]) -> Tuple[int, int]:
    step: int = 0
    span_platform: List[str] = platform
    state = "".join(span_platform)
    step_by_states: Dict[str, int] = {}
    while step == 0 or state not in step_by_states:
        step_by_states[state] = step
        span_platform = spin(span_platform)
        state = "".join(span_platform)
        step += 1
    return step_by_states[state], step


def spin(platform: List[str]) -> List[str]:
    return tilt_east(tilt_south(tilt_west(tilt_north(platform))))
