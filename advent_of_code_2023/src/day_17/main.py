import os

from src.day_17.clumsy_crucible import compute_least_heat_loss, compute_least_heat_loss_ultra
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: list[str] = read_lines_from_file(filename)
    print(f"Least heat loss: {compute_least_heat_loss(lines)}")
    print(f"Least heat ultra crucible loss: {compute_least_heat_loss_ultra(lines)}")
