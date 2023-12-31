import os

from src.day_4.scratchcards import compute_nb_cards, compute_sum_of_points
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines = read_lines_from_file(filename)
    print(f"Sum of points: {compute_sum_of_points(lines)}")
    print(f"Sum of points: {compute_nb_cards(lines)}")
