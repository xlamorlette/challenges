from typing import Final, List

from src.day_3.gear_ratios import LocatedNumber, Position, Schematic, compute_sum_of_gear_ratios, \
    compute_sum_of_part_numbers

SCHEMATIC_LINES: Final[List[str]] = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598.."
]

SCHEMATIC_LINES_BIS: Final[List[str]] = [
    "12.......*..",
    "+.........34",
    ".......-12..",
    "..78........",
    "..*....60...",
    "78..........",
    ".......23...",
    "....90*12...",
    "............",
    "2.2......12.",
    ".*.........*",
    "1.1.......56"
]


def test_compute_sum_of_part_numbers():
    assert compute_sum_of_part_numbers(SCHEMATIC_LINES) == 4361


def test_compute_sum_of_part_numbers_bis():
    assert compute_sum_of_part_numbers(SCHEMATIC_LINES_BIS) == 413


def test_get_part_numbers_ids():
    schematic = Schematic(SCHEMATIC_LINES)
    assert schematic.get_part_numbers_ids() == [467, 35, 633, 617, 592, 755, 664, 598]


def test_get_part_numbers_ids_bis():
    schematic = Schematic(SCHEMATIC_LINES_BIS)
    assert schematic.get_part_numbers_ids() == [12, 34, 12, 78, 78, 23, 90, 12, 2, 2, 12, 1, 1, 56]


def test_schematic_init():
    schematic = Schematic(SCHEMATIC_LINES)
    assert schematic.nb_rows == 10
    assert schematic.nb_columns == 10
    assert schematic.row_strings == SCHEMATIC_LINES


def test_schematic_get_numbers():
    schematic = Schematic(SCHEMATIC_LINES)
    assert schematic.get_numbers() == [
        LocatedNumber(467, Position(0, 0)),
        LocatedNumber(114, Position(0, 5)),
        LocatedNumber(35, Position(2, 2)),
        LocatedNumber(633, Position(2, 6)),
        LocatedNumber(617, Position(4, 0)),
        LocatedNumber(58, Position(5, 7)),
        LocatedNumber(592, Position(6, 2)),
        LocatedNumber(755, Position(7, 6)),
        LocatedNumber(664, Position(9, 1)),
        LocatedNumber(598, Position(9, 5))
    ]


def test_schematic_get_numbers_bis():
    schematic = Schematic(SCHEMATIC_LINES_BIS)
    numbers = schematic.get_numbers()
    assert LocatedNumber(34, Position(1, 10)) in numbers
    assert LocatedNumber(56, Position(11, 10)) in numbers


def test_schematic_is_part():
    schematic = Schematic(SCHEMATIC_LINES)
    assert schematic.is_part(LocatedNumber(467, Position(0, 0)))
    assert not schematic.is_part(LocatedNumber(114, Position(0, 5)))
    assert schematic.is_part(LocatedNumber(35, Position(2, 2)))
    assert schematic.is_part(LocatedNumber(633, Position(2, 6)))
    assert schematic.is_part(LocatedNumber(617, Position(4, 0)))
    assert not schematic.is_part(LocatedNumber(58, Position(5, 7)))
    assert schematic.is_part(LocatedNumber(592, Position(6, 2)))
    assert schematic.is_part(LocatedNumber(755, Position(7, 6)))
    assert schematic.is_part(LocatedNumber(664, Position(9, 1)))
    assert schematic.is_part(LocatedNumber(598, Position(9, 5)))


def test_schematic_is_symbol():
    assert Schematic.is_symbol("*")
    assert not Schematic.is_symbol("1")
    assert not Schematic.is_symbol(".")


def test_compute_sum_of_gear_ratios():
    assert compute_sum_of_gear_ratios(SCHEMATIC_LINES) == 467835


def test_compute_sum_of_gear_ratios_bis():
    assert compute_sum_of_gear_ratios(SCHEMATIC_LINES_BIS) == 6756


def test_schematic_get_gear_ratios():
    schematic = Schematic(SCHEMATIC_LINES)
    assert schematic.get_gear_ratios() == [16345, 451490]


def test_schematic_get_adjacent_part_numbers():
    schematic = Schematic(SCHEMATIC_LINES)
    numbers = schematic.get_numbers()
    assert schematic.get_adjacent_part_numbers(Position(1, 3), numbers) == [467, 35]
    assert schematic.get_adjacent_part_numbers(Position(0, 9), numbers) == []


def test_schematic_is_adjacent():
    assert not Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(4, 3)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(4, 4)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(4, 5)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(4, 6)))
    assert not Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(4, 7)))

    assert not Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(5, 3)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(5, 4)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(5, 6)))
    assert not Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(5, 7)))

    assert not Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(6, 3)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(6, 4)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(6, 5)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(6, 6)))
    assert not Schematic.is_adjacent(Position(5, 5), LocatedNumber(1, Position(6, 7)))

    assert not Schematic.is_adjacent(Position(5, 5), LocatedNumber(12, Position(4, 2)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(12, Position(4, 3)))

    assert not Schematic.is_adjacent(Position(5, 5), LocatedNumber(12, Position(5, 2)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(12, Position(5, 3)))
    assert Schematic.is_adjacent(Position(5, 5), LocatedNumber(12, Position(5, 6)))
    assert not Schematic.is_adjacent(Position(5, 5), LocatedNumber(12, Position(5, 7)))
