from typing import Final, List

from src.day_8.haunted_wasteland import Node, compute_nb_steps, compute_nb_steps_parallel_paths, get_start_node_names, \
    read_nodes_by_name

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


INPUT_3: Final[str] = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

INPUT_3_LINES: Final[List[str]] = INPUT_3.split("\n")


def test_compute_nb_steps__parallel_paths():
    assert compute_nb_steps_parallel_paths(INPUT_1_LINES) == 2
    assert compute_nb_steps_parallel_paths(INPUT_2_LINES) == 6
    assert compute_nb_steps_parallel_paths(INPUT_3_LINES) == 6


def test_get_start_node_names():
    nodes_by_name = read_nodes_by_name(INPUT_3_LINES[2:])
    assert get_start_node_names(nodes_by_name) == ["11A", "22A"]
