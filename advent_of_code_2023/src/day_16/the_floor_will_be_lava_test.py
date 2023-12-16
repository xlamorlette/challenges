from typing import Final, List

from src.day_16.the_floor_will_be_lava import Beam, Contraption, compute_maximum_energized_tiles_number, \
    compute_energized_tiles_number
from src.util.position import Position, NORTH, SOUTH, EAST, WEST

INPUT: Final[str] = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")


def test_compute_energized_tiles_number():
    assert compute_energized_tiles_number(INPUT_LINES) == 46


def test_contraption_get_next_beams():
    contraption = Contraption(INPUT_LINES)
    assert contraption.get_next_beams(Beam(Position(0, 0), EAST)) == [Beam(Position(0, 1), EAST)]
    assert contraption.get_next_beams(Beam(Position(0, 0), SOUTH)) == [Beam(Position(1, 0), SOUTH)]
    assert contraption.get_next_beams(Beam(Position(0, 0), NORTH)) == []
    assert contraption.get_next_beams(Beam(Position(0, 0), WEST)) == []
    assert contraption.get_next_beams(Beam(Position(2, 5), WEST)) == [Beam(Position(1, 5), NORTH),
                                                                      Beam(Position(3, 5), SOUTH)]
    assert contraption.get_next_beams(Beam(Position(1, 2), SOUTH)) == [Beam(Position(1, 3), EAST),
                                                                       Beam(Position(1, 1), WEST)]
    assert contraption.get_next_beams(Beam(Position(0, 5), EAST)) == [Beam(Position(1, 5), SOUTH)]
    assert contraption.get_next_beams(Beam(Position(6, 4), SOUTH)) == [Beam(Position(6, 3), WEST)]


def test_contraption_propagate_beam():
    contraption = Contraption(INPUT_LINES)
    contraption.propagate_beam()
    assert contraption.visited_cells[0][0] == {EAST}
    assert contraption.visited_cells[0][2] == {WEST}
    assert contraption.visited_cells[7][1] == {SOUTH, NORTH}


def test_compute_maximum_energized_tiles_number():
    assert compute_maximum_energized_tiles_number(INPUT_LINES) == 51
