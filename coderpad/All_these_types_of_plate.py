from dataclasses import dataclass
from enum import Enum, unique
from typing import Tuple


@unique
class PlateType(Enum):
    FLOWER_DECORATED = 0
    LIGHT_GREEN = 1
    BIG_BLUE = 2


@dataclass
class PlateGroup:
    plate_type: PlateType
    plates_number: int


class PlatePile:
    plate_groups: list[PlateGroup]

    def __init__(self):
        self.plate_groups = []

    def display(self):
        print("\n".join(str(group) for group in self.plate_groups))

    def set(self,
            plates: list[PlateType]):
        self.plate_groups = []
        for plate in plates:
            self.add([plate])

    # Add 1 or 2 plates
    # return the insertion index, and if the plates must be reversed
    def add(self,
            plates: list[PlateType]) -> Tuple[int, bool]:
        if len(plates) == 1:
            return self._add_one_plate(plates[0])
        if len(plates) != 2:
            # TODO: test
            raise RuntimeError(f"Invalid number of plates to add: {len(plates)}")
        # TODO: extract
        if plates[0] == plates[1]:
            return self._add_couple_same_plate(plates[0])
        else:
            return self._add_couple_different_plates(plates[0], plates[1])
        # TODO: test empty pile with two plates
        # TODO: test non-existing group
        assert False

    def _add_one_plate(self,
                       plate: PlateType) -> Tuple[int, bool]:
        for plate_group in self.plate_groups:
            if plate_group.plate_type == plate:
                plate_group.plates_number += 1
                # TODO: return correct index 
                return 0, False
        self.plate_groups.append(PlateGroup(plate, 1))
        # TODO: return correct index 
        return 0, False

    def _add_couple_same_plate(self,
                               plate: PlateType) -> Tuple[int, bool]:
        index = 0
        for plate_group in self.plate_groups:
            if plate_group.plate_type == plate:
                plate_group.plates_number += 2
                return index, False
            index += plate_group.plates_number
        # TODO: non-existing group
        assert False

    def _add_couple_different_plates(self,
                                     plate_1: PlateType,
                                     plate_2: PlateType) -> Tuple[int, bool]:
        index = 0
        for group_index in range(len(self.plate_groups) - 1):
            index += self.plate_groups[group_index].plates_number
            found = False
            reverse = False
            if self.plate_groups[group_index].plate_type == plate_1 \
                    and self.plate_groups[group_index + 1].plate_type == plate_2:
                found = True
                # TODO: test with no reverse
            if self.plate_groups[group_index].plate_type == plate_2 \
                    and self.plate_groups[group_index + 1].plate_type == plate_1:
                found = True
                reverse = True
            if found:
                self.plate_groups[group_index].plates_number += 1
                self.plate_groups[group_index + 1].plates_number += 1
                return index, reverse
        assert False


def test_example_scenario():
    pile_initial_state: list[PlateType] = [
        PlateType.FLOWER_DECORATED,
        PlateType.LIGHT_GREEN,
        PlateType.LIGHT_GREEN,
        PlateType.BIG_BLUE,
        PlateType.BIG_BLUE
    ]
    pile = PlatePile()
    pile.set(pile_initial_state)
    pile.display()
    assert pile.add([PlateType.LIGHT_GREEN, PlateType.LIGHT_GREEN]) == (1, False)
    pile.display()
    assert pile.add([PlateType.BIG_BLUE, PlateType.LIGHT_GREEN]) == (5, True)


if __name__ == "__main__":
    test_example_scenario()
    print("done")

