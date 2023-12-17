from typing import Final

from src.day_17.clumsy_crucible import compute_least_heat_loss


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

INPUT_LINES: Final[list[str]] = INPUT.split("\n")


def test_compute_least_heat_loss():
    assert compute_least_heat_loss(INPUT_LINES) == 102
