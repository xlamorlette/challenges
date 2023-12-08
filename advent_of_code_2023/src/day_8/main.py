import os
from typing import List

from src.day_8.haunted_wasteland import compute_nb_steps, compute_nb_steps_parallel_paths
from src.util.file import read_lines_from_file


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines: List[str] = read_lines_from_file(filename)
    print(f"Number of steps required: {compute_nb_steps(lines)}")
    print(f"Number of steps required for parallel paths: {compute_nb_steps_parallel_paths(lines)}")
