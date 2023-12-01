#!/usr/bin/env python3

from typing import List


def read_file(_calibration_file: str) -> List[str]:
    return []


def compute_calibration_sum(_calibration_data: List[str]) -> int:
    return 0


if __name__ == "__main__":
    calibration_data = read_file("input.txt")
    result = compute_calibration_sum(calibration_data)
    print(f"Sum of the calibration values: {result}")
