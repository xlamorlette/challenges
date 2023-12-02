import os

from src.util.file import read_lines_from_file


def test_read_lines_from_file():
    current_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_path, "input.txt")
    lines = read_lines_from_file(filename)
    assert lines == [
        "threehqv2",
        "sxoneightoneckk9ldctxxnffqnzmjqvj",
        "1hggcqcstgpmg26lzxtltcgg"
    ]
