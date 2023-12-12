import os
from typing import List

from src.day_12.hot_springs import compute_sum_of_broken_spring_arrangements, \
    compute_sum_of_broken_spring_arrangements_unfolded
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Sum of broken springs arrangements: {compute_sum_of_broken_spring_arrangements(lines)}")
    print(f"Sum of broken springs arrangements unfolded: {compute_sum_of_broken_spring_arrangements_unfolded(lines)}")
