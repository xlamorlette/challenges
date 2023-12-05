import os

from src.day_5.seed_almanac import SeedAlmanac, SeedAlmanac2
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines = read_lines_from_file(filename)
    print(f"Lowest location: {SeedAlmanac(lines).compute_lowest_location()}")
    print(f"Lowest location 2: {SeedAlmanac2(lines).compute_lowest_location()}")
