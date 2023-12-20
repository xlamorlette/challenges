from typing import Final

from src.day_20.pulse_propagation import compute_pulses_number_product

INPUT: Final[str] = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

INPUT_2: Final[str] = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

INPUT_LINES: Final[list[str]] = INPUT.split("\n")
INPUT_2_LINES: Final[list[str]] = INPUT_2.split("\n")


def test_compute_pulses_number_product():
    assert compute_pulses_number_product(INPUT_LINES) == 32000000
    assert compute_pulses_number_product(INPUT_2_LINES) == 11687500
