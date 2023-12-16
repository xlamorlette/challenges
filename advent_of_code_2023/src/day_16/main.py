import os
from typing import List

from src.day_16.the_floor_will_be_lava import compute_energized_tiles_number, compute_maximum_energized_tiles_number
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Number of energized tiles: {compute_energized_tiles_number(lines)}")
    print(f"Maximum number of energized tiles: {compute_maximum_energized_tiles_number(lines)}")
