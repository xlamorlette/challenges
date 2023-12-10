import os
from typing import List

from src.day_10.pipe_maze import compute_farthest_distance, get_nb_enclosed_tiles
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Steps to the farthest position: {compute_farthest_distance(lines)}")
    print(f"Number of enclosed tiles: {get_nb_enclosed_tiles(lines)}")
