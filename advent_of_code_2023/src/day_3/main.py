import os

from src.day_3.gear_ratios import compute_sum_of_gear_ratios, compute_sum_of_part_numbers
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines = read_lines_from_file(filename)
    result = compute_sum_of_part_numbers(lines)
    print(f"Sum of the part numbers: {result}")
    result = compute_sum_of_gear_ratios(lines)
    print(f"Sum of the gear ratios: {result}")
