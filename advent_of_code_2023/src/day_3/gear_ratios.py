import math
import re
from dataclasses import dataclass
from typing import List


@dataclass
class NumberInGrid:
    number: int
    row: int
    column: int

    def get_length(self) -> int:
        return len(str(self.number))


class Schematic:
    nb_rows: int
    nb_columns: int
    row_strings: List[str]

    def __init__(self,
                 schematic_lines: List[str]):
        self.nb_rows = len(schematic_lines)
        self.nb_columns = len(schematic_lines[0])
        self.row_strings = schematic_lines

    def get_part_numbers_ids(self) -> List[int]:
        located_numbers_list = self.get_numbers()
        return [located_number.number for located_number in located_numbers_list if self.is_part(located_number)]

    def get_numbers(self) -> List[NumberInGrid]:
        numbers_list: List[NumberInGrid] = []
        for row, row_string in enumerate(self.row_strings):
            for match in re.finditer(r"\d+", row_string):
                number = int(match.group())
                column = match.start()
                numbers_list.append(NumberInGrid(number, row, column))
        return numbers_list

    def is_part(self,
                number: NumberInGrid) -> bool:
        min_row = max(0, number.row - 1)
        max_row = min(self.nb_rows - 1, number.row + 1)
        min_column = max(0, number.column - 1)
        max_column = min(self.nb_columns - 1, number.column + number.get_length())
        return any(self.is_symbol(self.row_strings[row][column])
                   for row in range(min_row, max_row + 1)
                   for column in range(min_column, max_column + 1))

    @staticmethod
    def is_symbol(character: str) -> bool:
        return (not character.isdigit()) and (character != ".")

    @staticmethod
    def is_gear_symbol(character: str) -> bool:
        return character == "*"

    def get_gear_ratios(self) -> List[int]:
        gear_ratios_list = []
        numbers_list = self.get_numbers()
        for row in range(self.nb_rows):
            for column in range(self.nb_columns):
                if self.is_gear_symbol(self.row_strings[row][column]):
                    part_numbers = self.get_adjacent_part_numbers(row, column, numbers_list)
                    if len(part_numbers) == 2:
                        gear_ratio = math.prod(part_numbers)
                        gear_ratios_list.append(gear_ratio)
        return gear_ratios_list

    def get_adjacent_part_numbers(self,
                                  row: int,
                                  column: int,
                                  numbers_list: List[NumberInGrid]) -> List[int]:
        return [number.number for number in numbers_list if self.is_adjacent(row, column, number)]

    @staticmethod
    def is_adjacent(row: int,
                    column: int,
                    number: NumberInGrid) -> bool:
        min_row = number.row - 1
        max_row = number.row + 1
        min_column = number.column - 1
        max_column = number.column + number.get_length()
        return min_row <= row <= max_row \
            and min_column <= column <= max_column


def compute_sum_of_part_numbers(schematic_lines: List[str]) -> int:
    schematic = Schematic(schematic_lines)
    part_numbers_ids = schematic.get_part_numbers_ids()
    return sum(part_numbers_ids)


def compute_sum_of_gear_ratios(schematic_lines: List[str]) -> int:
    schematic = Schematic(schematic_lines)
    gear_ratios = schematic.get_gear_ratios()
    return sum(gear_ratios)
