from typing import Final, List

from src.day_8.haunted_wasteland import Node, compute_nb_steps, read_nodes_by_name

INPUT_1: Final[str] = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

INPUT_1_LINES: Final[List[str]] = INPUT_1.split("\n")


INPUT_2: Final[str] = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

INPUT_2_LINES: Final[List[str]] = INPUT_2.split("\n")


def test_compute_nb_steps():
    assert compute_nb_steps(INPUT_1_LINES) == 2
    assert compute_nb_steps(INPUT_2_LINES) == 6


def test_read_nodes_by_name():
    assert read_nodes_by_name(INPUT_2_LINES[2:]) == {
        "AAA": Node("AAA", "BBB", "BBB"),
        "BBB": Node("BBB", "AAA", "ZZZ"),
        "ZZZ": Node("ZZZ", "ZZZ", "ZZZ")
    }
