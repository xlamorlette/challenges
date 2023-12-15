from typing import Final

from src.day_15.lens_library import compute_sum_of_hashes, get_hash

INPUT: Final[str] = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_compute_sum_of_hashes():
    assert compute_sum_of_hashes(INPUT) == 1320


def test_get_hash():
    assert get_hash("HASH") == 52
    assert get_hash("rn=1") == 30
