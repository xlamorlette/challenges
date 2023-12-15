import functools
from dataclasses import dataclass
from typing import List


def compute_sum_of_hashes(line: str) -> int:
    return sum(map(get_hash, line.split(',')))


def get_hash(step: str) -> int:
    return functools.reduce(lambda value, character: ((value + ord(character)) * 17) % 256, step, 0)


@dataclass
class Lens:
    label: str
    focal_length: int


class Box:
    lenses: List[Lens]

    def __init__(self):
        self.lenses = []

    def get_focusing_power_sum(self) -> int:
        return sum((index + 1) * lens.focal_length for index, lens in enumerate(self.lenses))

    def apply_step(self,
                   step: str):
        if "=" in step:
            label, focal_length = step.split("=")
            self.add_lens(label, int(focal_length))
        if "-" in step:
            label = step.split("-")[0]
            self.remove_lens(label)

    def add_lens(self,
                 label: str,
                 focal_length: int):
        for lens in self.lenses:
            if lens.label == label:
                lens.focal_length = focal_length
                return
        self.lenses.append(Lens(label, focal_length))

    def remove_lens(self,
                    label: str):
        self.lenses = list(filter(lambda lens: lens.label != label, self.lenses))


class Library:
    boxes: List[Box]

    def __init__(self):
        self.boxes = [Box() for _index in range(256)]

    def get_focusing_power_sum(self) -> int:
        return sum((index + 1) * box.get_focusing_power_sum() for index, box in enumerate(self.boxes))

    def apply_step(self,
                   step: str):
        label = step.replace("=", "-").split("-")[0]
        self.boxes[get_hash(label)].apply_step(step)


def compute_focusing_power_sum(line: str) -> int:
    library: Library = Library()
    for step in line.split(","):
        library.apply_step(step)
    return library.get_focusing_power_sum()
