import math
from dataclasses import dataclass
from typing import List


@dataclass
class Position:
    row: int
    column: int


@dataclass
class LocatedNumber:
    number: int
    position: Position


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

    def get_numbers(self) -> List[LocatedNumber]:
        numbers_list: List[LocatedNumber] = []
        for row, row_string in enumerate(self.row_strings):
            buffer: str = ""
            for column in range(self.nb_columns):
                character = row_string[column]
                if character.isdigit():
                    buffer += character
                else:
                    if buffer != "":
                        number = int(buffer)
                        number_column_id = column - len(buffer)
                        numbers_list.append(LocatedNumber(number, Position(row=row, column=number_column_id)))
                        buffer = ""
            if buffer != "":
                number = int(buffer)
                number_column_id = self.nb_columns - len(buffer)
                numbers_list.append(LocatedNumber(number, Position(row=row, column=number_column_id)))
        return numbers_list

    def is_part(self,
                number: LocatedNumber) -> bool:
        min_row = max(0, number.position.row - 1)
        max_row = min(self.nb_rows - 1, number.position.row + 1)
        min_column = max(0, number.position.column - 1)
        max_column = min(self.nb_columns - 1, number.position.column + len(str(number.number)))
        for row in range(min_row, max_row + 1):
            for column in range(min_column, max_column + 1):
                if self.is_symbol(self.row_strings[row][column]):
                    return True
        return False

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
                    part_numbers = self.get_adjacent_part_numbers(Position(row=row, column=column), numbers_list)
                    if len(part_numbers) == 2:
                        gear_ratio = math.prod(part_numbers)
                        gear_ratios_list.append(gear_ratio)
        return gear_ratios_list

    def get_adjacent_part_numbers(self,
                                  position: Position,
                                  numbers_list: List[LocatedNumber]) -> List[int]:
        return [number.number for number in numbers_list if self.is_adjacent(position, number)]

    @staticmethod
    def is_adjacent(position: Position,
                    number: LocatedNumber) -> bool:
        number_length = len(str(number.number))
        min_row = number.position.row - 1
        max_row = number.position.row + 1
        min_column = number.position.column - 1
        max_column = number.position.column + number_length
        return min_row <= position.row <= max_row \
            and min_column <= position.column <= max_column


def compute_sum_of_part_numbers(schematic_lines: List[str]) -> int:
    schematic = Schematic(schematic_lines)
    part_numbers_ids = schematic.get_part_numbers_ids()
    return sum(part_numbers_ids)


def compute_sum_of_gear_ratios(schematic_lines: List[str]) -> int:
    schematic = Schematic(schematic_lines)
    gear_ratios = schematic.get_gear_ratios()
    return sum(gear_ratios)
