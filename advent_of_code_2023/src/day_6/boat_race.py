import math
from typing import List


def compute_number_of_ways_to_win(lines: List[str]) -> int:
    times, distances = [list(map(int, line.split(":")[1].split())) for line in lines]
    return math.prod(compute_number_of_winning_races(time, distance) for time, distance in zip(times, distances))


def compute_number_of_winning_races(race_time: int,
                                    best_distance: int) -> int:
    return sum(compute_distance(button_time, race_time) > best_distance for button_time in range(race_time))


def compute_distance(button_time: int,
                     race_time: int) -> int:
    speed: int = button_time
    moving_time: int = race_time - button_time
    return speed * moving_time


def compute_number_of_ways_to_win_2(lines: List[str]) -> int:
    time, distance = [int("".join(line.split(":")[1].split())) for line in lines]
    delta: int = time ** 2 - 4 * distance
    square_root_delta: float = math.sqrt(delta)
    first_root = (time - square_root_delta) / 2
    second_root = (time + square_root_delta) / 2
    return math.floor(second_root) - math.ceil(first_root) + 1
