import os

from src.day_19.aplenty import compute_accepted_parts_rating_sum, compute_number_of_accepted_combinations
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: list[str] = read_lines_from_file(filename)
    print(f"Sum of rating of accepted parts: {compute_accepted_parts_rating_sum(lines)}")
    print(f"Number of accepted combinations: {compute_number_of_accepted_combinations(lines)}")
