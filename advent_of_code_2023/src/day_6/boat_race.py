import math
from typing import List


def compute_number_of_ways_to_win(lines: List[str]) -> int:
    times: List[int] = list(map(int, lines[0].split(":")[1].split()))
    distances: List[int] = list(map(int, lines[1].split(":")[1].split()))
    return math.prod(compute_number_of_ways_to_win_race(times[race_index], distances[race_index])
                     for race_index in range(len(times)))


def compute_number_of_ways_to_win_race(race_time: int,
                                       best_distance: int) -> int:
    winning_races = 0
    for button_time in range(race_time):
        if compute_distance(button_time, race_time) > best_distance:
            winning_races += 1
    return winning_races


def compute_distance(button_time: int,
                     race_time: int) -> int:
    speed: int = button_time
    moving_time: int = race_time - button_time
    return speed * moving_time


def compute_number_of_ways_to_win_2(lines: List[str]) -> int:
    time: int = int("".join(lines[0].split(":")[1].split()))
    distance: int = int("".join(lines[1].split(":")[1].split()))
    return compute_number_of_ways_to_win_race(time, distance)
