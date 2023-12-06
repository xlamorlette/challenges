import os
from typing import List

from src.day_6.boat_race import compute_number_of_ways_to_win
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Number of ways to win: {compute_number_of_ways_to_win(lines)}")
