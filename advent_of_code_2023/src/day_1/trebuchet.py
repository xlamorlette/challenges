#!/usr/bin/env python3
from typing import List


def read_file(calibration_file: str) -> List[str]:
    data: List[str] = []
    with open(calibration_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip()
            data.append(line)
    return data


def get_first_digit(line: str) -> int:
    for character in line:
        if character.isdigit():
            return int(character)
    raise RuntimeError("no digit found")


def get_last_digit(line: str) -> int:
    for character in reversed(line):
        if character.isdigit():
            return int(character)
    raise RuntimeError("no digit found")


def get_calibration_value(line: str) -> int:
    first_digit: int = get_first_digit(line)
    last_digit: int = get_last_digit(line)
    return first_digit * 10 + last_digit


def compute_calibration_sum(calibration_data: List[str]) -> int:
    return sum(get_calibration_value(line) for line in calibration_data)


if __name__ == "__main__":
    file_data = read_file("input.txt")
    result = compute_calibration_sum(file_data)
    print(f"Sum of the calibration values: {result}")
