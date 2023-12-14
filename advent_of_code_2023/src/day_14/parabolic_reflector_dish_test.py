from typing import Final, List

from src.day_14.parabolic_reflector_dish import compute_one_billion_spins_load, compute_total_load, get_platform_load, \
    get_spin_cycle, spin, tilt_east, tilt_line, tilt_north, tilt_south, tilt_west

INPUT: Final[str] = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

TILTED_NORTH_PLATFORM_MULTILINE: Final[str] = """OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#...."""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")
TILTED_NORTH_PLATFORM: Final[List[str]] = TILTED_NORTH_PLATFORM_MULTILINE.split("\n")


def test_compute_total_load():
    assert compute_total_load(INPUT_LINES) == 136


def test_tilt_north():
    assert tilt_north(INPUT_LINES) == TILTED_NORTH_PLATFORM


def test_tilt_south():
    assert tilt_south(INPUT_LINES) == """.....#....
....#....#
...O.##...
...#......
O.O....O#O
O.#..O.#.#
O....#....
OO....OO..
#OO..###..
#OO.O#...O""".split("\n")


def test_tilt_west():
    assert tilt_west(INPUT_LINES) == """O....#....
OOO.#....#
.....##...
OO.#OO....
OO......#.
O.#O...#.#
O....#OO..
O.........
#....###..
#OO..#....""".split("\n")


def test_tilt_east():
    assert tilt_east(INPUT_LINES) == """....O#....
.OOO#....#
.....##...
.OO#....OO
......OO#.
.O#...O#.#
....O#..OO
.........O
#....###..
#..OO#....""".split("\n")


def test_tilt_line():
    assert tilt_line("OO.O.O..##") == "OOOO....##"
    assert tilt_line("...OO....O") == "OOO......."
    assert tilt_line(".O...#O..O") == "O....#OO.."
    assert tilt_line("#.#..O#.##") == "#.#O..#.##"
    assert tilt_line("....#.....") == "....#....."
    assert tilt_line(".#.O.#O...") == ".#O..#O..."


def test_get_platform_load():
    assert get_platform_load(TILTED_NORTH_PLATFORM) == 136


def test_compute_one_billion_spins_load():
    assert compute_one_billion_spins_load(INPUT_LINES) == 64


def test_get_spin_cycle():
    assert get_spin_cycle(INPUT_LINES) == (3, 10)


def test_spin():
    assert spin(INPUT_LINES) == """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....""".split("\n")
