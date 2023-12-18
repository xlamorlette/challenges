import os

from src.day_18.lavaduct_lagoon import compute_lagoon_capacity
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: list[str] = read_lines_from_file(filename)
    print(f"Lagoon capacity: {compute_lagoon_capacity(lines)}")
