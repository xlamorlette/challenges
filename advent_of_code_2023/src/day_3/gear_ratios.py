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
        # for number in located_numbers_list:
        #     if not self.is_part(number):
        #         print(f"{number}: {self.is_part(number)}")
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


def compute_sum_of_part_numbers(schematic_lines: List[str]) -> int:
    schematic = Schematic(schematic_lines)
    part_numbers_ids = schematic.get_part_numbers_ids()
    return sum(part_numbers_ids)
