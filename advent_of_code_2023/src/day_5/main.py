import os

from src.day_5.seed_almanac import SeedAlmanac
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines = read_lines_from_file(filename)
    almanac = SeedAlmanac(lines)
    print(f"Lowest location: {almanac.compute_lowest_location()}")
