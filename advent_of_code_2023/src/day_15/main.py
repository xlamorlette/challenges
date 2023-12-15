import os
from typing import List

from src.day_15.lens_library import compute_focusing_power_sum, compute_sum_of_hashes
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Sum of hashes: {compute_sum_of_hashes(lines[0])}")
    print(f"Focusing power sum: {compute_focusing_power_sum(lines[0])}")
