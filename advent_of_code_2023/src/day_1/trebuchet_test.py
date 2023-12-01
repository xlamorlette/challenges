import pytest

from src.day_1.trebuchet import compute_calibration_sum, get_calibration_value, get_first_digit, get_last_digit


def test_compute_calibration_sum():
    assert compute_calibration_sum([]) == 0
    assert compute_calibration_sum(["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]) == 142


def test_get_calibration_value():
    assert get_calibration_value("1abc2") == 12
    assert get_calibration_value("pqr3stu8vwx") == 38
    assert get_calibration_value("a1b2c3d4e5f") == 15
    assert get_calibration_value("treb7uchet") == 77


def test_get_first_digit():
    assert get_first_digit("1abc2") == 1
    assert get_first_digit("pqr3stu8vwx") == 3
    assert get_first_digit("a1b2c3d4e5f") == 1
    assert get_first_digit("treb7uchet") == 7
    with pytest.raises(RuntimeError, match="no digit found"):
        get_first_digit("")
    with pytest.raises(RuntimeError, match="no digit found"):
        get_first_digit("foo")


def test_get_last_digit():
    assert get_last_digit("1abc2") == 2
    assert get_last_digit("pqr3stu8vwx") == 8
    assert get_last_digit("a1b2c3d4e5f") == 5
    assert get_last_digit("treb7uchet") == 7
    with pytest.raises(RuntimeError, match="no digit found"):
        get_last_digit("")
    with pytest.raises(RuntimeError, match="no digit found"):
        get_last_digit("foo")
