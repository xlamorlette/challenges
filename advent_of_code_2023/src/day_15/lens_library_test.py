from typing import Final

from src.day_15.lens_library import Lens, Library, compute_focusing_power_sum, compute_sum_of_hashes, get_hash

INPUT: Final[str] = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_compute_sum_of_hashes():
    assert compute_sum_of_hashes(INPUT) == 1320


def test_get_hash():
    assert get_hash("HASH") == 52
    assert get_hash("rn=1") == 30


def test_compute_focusing_power_sum():
    assert compute_focusing_power_sum(INPUT) == 145


def test_library_get_focusing_power_sum():
    library: Library = Library()
    library.boxes[0].lenses = [Lens("rn", 1), Lens("cm", 2)]
    library.boxes[3].lenses = [Lens("ot", 7), Lens("ab", 5), Lens("pc", 6)]
    assert library.get_focusing_power_sum() == 145


def test_library_apply_step():
    library: Library = Library()
    library.apply_step("rn=1")
    assert library.boxes[0].lenses == [Lens("rn", 1)]
    library.apply_step("cm-")
    assert library.boxes[0].lenses == [Lens("rn", 1)]
    assert all(library.boxes[index].lenses == [] for index in range(1, 256))
    library.apply_step("qp=3")
    assert library.boxes[1].lenses == [Lens("qp", 3)]
    library.apply_step("cm=2")
    assert library.boxes[0].lenses == [Lens("rn", 1), Lens("cm", 2)]
    library.apply_step("qp-")
    assert library.boxes[1].lenses == []
    library.apply_step("pc=4")
    library.apply_step("ot=9")
    library.apply_step("ab=5")
    assert library.boxes[3].lenses == [Lens("pc", 4), Lens("ot", 9), Lens("ab", 5)]
    library.apply_step("pc-")
    library.apply_step("pc=6")
    library.apply_step("ot=7")
    assert library.boxes[3].lenses == [Lens("ot", 7), Lens("ab", 5), Lens("pc", 6)]
