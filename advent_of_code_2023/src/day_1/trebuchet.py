#!/usr/bin/env python3
from typing import Dict, List, Optional


def read_file(calibration_file: str) -> List[str]:
    data: List[str] = []
    with open(calibration_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip()
            data.append(line)
    return data


SPELLED_DIGITS: Dict[str, int] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def get_spelled_digit(line: str,
                      go_backward: bool = False) -> Optional[int]:
    for character_index in range(len(line)):
        substring = line[len(line) - character_index - 1:] if go_backward else line[character_index:]
        for spelled_digit, digit in SPELLED_DIGITS.items():
            if substring[:len(spelled_digit)] == spelled_digit:
                return digit
    return None


def get_first_digit(line: str) -> int:
    for character_index, character in enumerate(line):
        if character.isdigit():
            line_begining = line[:character_index]
            digit = get_spelled_digit(line_begining)
            if digit:
                return digit
            return int(character)
    raise RuntimeError("no digit found")


def get_last_digit(line: str) -> int:
    for character_index in range(len(line) - 1, -1, -1):
        character = line[character_index]
        if character.isdigit():
            line_ending = line[character_index + 1:]
            digit = get_spelled_digit(line_ending, go_backward=True)
            if digit:
                return digit
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
