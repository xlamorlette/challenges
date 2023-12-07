import os
from typing import List

from src.day_7.camel_cards import compute_total_winnings
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Total winnings: {compute_total_winnings(lines)}")
