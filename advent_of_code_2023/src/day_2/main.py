import os

from src.day_2.cube_conundrum import compute_possible_games_ids_sum
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines = read_lines_from_file(filename)
    result = compute_possible_games_ids_sum(lines)
    print(f"Sum of the IDs of the possible games: {result}")
