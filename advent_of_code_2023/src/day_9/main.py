import os
from typing import List

from src.day_9.mirage_maintenance import compute_extrapolated_values_sum
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Sum of extrapolated values: {compute_extrapolated_values_sum(lines)}")
