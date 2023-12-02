from typing import List


def read_lines_from_file(filename: str) -> List[str]:
    lines: List[str] = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(line.rstrip())
    return lines
