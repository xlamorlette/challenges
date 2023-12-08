from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Node:
    name: str
    left: str
    right: str

    def get_next_node_name(self,
                           direction: str) -> str:
        match direction:
            case "L":
                return self.left
            case "R":
                return self.right
        assert False, f"unexpected direction: {direction}"


def compute_nb_steps(lines: List[str]) -> int:
    instructions: str = lines[0]
    nodes_by_name: Dict[str, Node] = read_nodes_by_name(lines[2:])
    return get_path_length(instructions, nodes_by_name)


def read_nodes_by_name(node_lines: List[str]) -> Dict[str, Node]:
    nodes_by_name: Dict[str, Node] = {}
    for line in node_lines:
        elements = line.replace('=', '').replace('(', '').replace(',', '').replace(')', '').split()
        nodes_by_name[elements[0]] = Node(*elements)
    return nodes_by_name


def get_path_length(instructions: str,
                    nodes_by_name: Dict[str, Node]) -> int:
    nb_steps: int = 0
    current_node_name: str = "AAA"
    while current_node_name != "ZZZ":
        direction = get_direction(instructions, nb_steps)
        current_node_name = nodes_by_name[current_node_name].get_next_node_name(direction)
        nb_steps += 1
    return nb_steps


def get_direction(instructions: str,
                  step_index: int) -> str:
    instruction_index = step_index % len(instructions)
    return instructions[instruction_index]
