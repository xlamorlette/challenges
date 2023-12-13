import os
from typing import List

from src.day_13.point_of_incidence import compute_sum_of_reflection_numbers, compute_sum_of_smudged_reflection_numbers
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Sum of reflection numbers: {compute_sum_of_reflection_numbers(lines)}")
    print(f"Sum of smudged reflection numbers: {compute_sum_of_smudged_reflection_numbers(lines)}")
