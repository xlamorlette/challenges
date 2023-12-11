from src.util.position import Position


def test_manhattan_distance():
    assert Position(1, 2).manhattan_distance(Position(2, 4)) == 3
    assert Position(2, 4).manhattan_distance(Position(1, 2)) == 3
