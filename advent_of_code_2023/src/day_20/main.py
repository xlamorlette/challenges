import os

from src.day_20.pulse_propagation import compute_pulses_number_product
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: list[str] = read_lines_from_file(filename)
    print(f"Product of number of pulses: {compute_pulses_number_product(lines)}")
