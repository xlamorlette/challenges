from typing import Final

from src.day_17.clumsy_crucible import compute_least_heat_loss, compute_least_heat_loss_ultra


INPUT: Final[str] = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

INPUT_2: Final[str] = """111111111111
999999999991
999999999991
999999999991
999999999991"""

INPUT_LINES: Final[list[str]] = INPUT.split("\n")
INPUT_LINES_2: Final[list[str]] = INPUT_2.split("\n")


def test_compute_least_heat_loss():
    assert compute_least_heat_loss(INPUT_LINES) == 102


def test_compute_least_heat_loss_ultra():
    assert compute_least_heat_loss_ultra(INPUT_LINES) == 94
    assert compute_least_heat_loss_ultra(INPUT_LINES_2) == 71
