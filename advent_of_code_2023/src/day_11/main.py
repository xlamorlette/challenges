import os
from typing import List

from src.day_11.cosmic_expansion import compute_sum_of_pair_distances
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Sum of pair distances: {compute_sum_of_pair_distances(lines)}")
    print(f"Sum of pair distances with 1 million expansion factor: {compute_sum_of_pair_distances(lines, 1000000)}")
