from typing import Final, List

from src.day_3.gear_ratios import NumberInGrid, Schematic, compute_sum_of_gear_ratios, \
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
        NumberInGrid(467, 0, 0),
        NumberInGrid(114, 0, 5),
        NumberInGrid(35, 2, 2),
        NumberInGrid(633, 2, 6),
        NumberInGrid(617, 4, 0),
        NumberInGrid(58, 5, 7),
        NumberInGrid(592, 6, 2),
        NumberInGrid(755, 7, 6),
        NumberInGrid(664, 9, 1),
        NumberInGrid(598, 9, 5)
    ]


def test_schematic_get_numbers_bis():
    schematic = Schematic(SCHEMATIC_LINES_BIS)
    numbers = schematic.get_numbers()
    assert NumberInGrid(34, 1, 10) in numbers
    assert NumberInGrid(56, 11, 10) in numbers


def test_schematic_is_part():
    schematic = Schematic(SCHEMATIC_LINES)
    assert schematic.is_part(NumberInGrid(467, 0, 0))
    assert not schematic.is_part(NumberInGrid(114, 0, 5))
    assert schematic.is_part(NumberInGrid(35, 2, 2))
    assert schematic.is_part(NumberInGrid(633, 2, 6))
    assert schematic.is_part(NumberInGrid(617, 4, 0))
    assert not schematic.is_part(NumberInGrid(58, 5, 7))
    assert schematic.is_part(NumberInGrid(592, 6, 2))
    assert schematic.is_part(NumberInGrid(755, 7, 6))
    assert schematic.is_part(NumberInGrid(664, 9, 1))
    assert schematic.is_part(NumberInGrid(598, 9, 5))


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
    assert schematic.get_adjacent_part_numbers(1, 3, numbers) == [467, 35]
    assert schematic.get_adjacent_part_numbers(0, 9, numbers) == []


def test_schematic_is_adjacent():
    assert not Schematic.is_adjacent(5, 5, NumberInGrid(1, 4, 3))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(1, 4, 4))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(1, 4, 5))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(1, 4, 6))
    assert not Schematic.is_adjacent(5, 5, NumberInGrid(1, 4, 7))

    assert not Schematic.is_adjacent(5, 5, NumberInGrid(1, 5, 3))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(1, 5, 4))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(1, 5, 6))
    assert not Schematic.is_adjacent(5, 5, NumberInGrid(1, 5, 7))

    assert not Schematic.is_adjacent(5, 5, NumberInGrid(1, 6, 3))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(1, 6, 4))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(1, 6, 5))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(1, 6, 6))
    assert not Schematic.is_adjacent(5, 5, NumberInGrid(1, 6, 7))

    assert not Schematic.is_adjacent(5, 5, NumberInGrid(12, 4, 2))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(12, 4, 3))

    assert not Schematic.is_adjacent(5, 5, NumberInGrid(12, 5, 2))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(12, 5, 3))
    assert Schematic.is_adjacent(5, 5, NumberInGrid(12, 5, 6))
    assert not Schematic.is_adjacent(5, 5, NumberInGrid(12, 5, 7))
