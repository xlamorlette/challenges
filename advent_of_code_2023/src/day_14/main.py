import os
from typing import List

from src.day_14.parabolic_reflector_dish import compute_total_load
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Total load: {compute_total_load(lines)}")
