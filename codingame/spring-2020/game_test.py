from game import Position


def test_position_manhattan_distance():
    assert Position(1, 2).manhattan_distance(Position(2, 4)) == 3
    assert Position(2, 4).manhattan_distance(Position(1, 2)) == 3


def test_position_mathematical_operations():
    assert Position(1, 2) + Position(3, 4) == Position(4, 6)
    assert Position(1, 2) * 2 == Position(2, 4)
