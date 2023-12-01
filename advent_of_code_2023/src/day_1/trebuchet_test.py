import pytest

from src.day_1.trebuchet import compute_calibration_sum, get_calibration_value, get_first_digit, get_last_digit, \
    get_spelled_digit


def test_compute_calibration_sum():
    assert compute_calibration_sum([]) == 0
    assert compute_calibration_sum(["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]) == 142


def test_get_calibration_value():
    assert get_calibration_value("1abc2") == 12
    assert get_calibration_value("pqr3stu8vwx") == 38
    assert get_calibration_value("a1b2c3d4e5f") == 15
    assert get_calibration_value("treb7uchet") == 77


def test_get_calibration_value_with_spelled_digits():
    assert get_calibration_value("two1nine") == 29
    assert get_calibration_value("abcone2threexyz") == 13
    assert get_calibration_value("xtwone3four") == 24
    assert get_calibration_value("4nineeightseven2") == 42
    assert get_calibration_value("zoneight234") == 14
    assert get_calibration_value("7pqrstsixteen") == 76
    assert get_calibration_value("1twone") == 11


def test_get_first_digit():
    assert get_first_digit("1abc2") == 1
    assert get_first_digit("pqr3stu8vwx") == 3
    assert get_first_digit("a1b2c3d4e5f") == 1
    assert get_first_digit("treb7uchet") == 7
    with pytest.raises(RuntimeError, match="no digit found"):
        get_first_digit("")
    with pytest.raises(RuntimeError, match="no digit found"):
        get_first_digit("foo")


def test_get_first_digit_with_spelled_digits():
    assert get_first_digit("two1nine") == 2
    assert get_first_digit("abcone2threexyz") == 1
    assert get_first_digit("xtwone3four") == 2
    assert get_first_digit("4nineeightseven2") == 4
    assert get_first_digit("zoneight234") == 1
    assert get_first_digit("7pqrstsixteen") == 7


def test_get_last_digit():
    assert get_last_digit("1abc2") == 2
    assert get_last_digit("pqr3stu8vwx") == 8
    assert get_last_digit("a1b2c3d4e5f") == 5
    assert get_last_digit("treb7uchet") == 7
    with pytest.raises(RuntimeError, match="no digit found"):
        get_last_digit("")
    with pytest.raises(RuntimeError, match="no digit found"):
        get_last_digit("foo")


def test_get_last_digit_with_spelled_digits():
    assert get_last_digit("two1nine") == 9
    assert get_last_digit("abcone2threexyz") == 3
    assert get_last_digit("xtwone3four") == 4
    assert get_last_digit("4nineeightseven2") == 2
    assert get_last_digit("zoneight234") == 4
    assert get_last_digit("7pqrstsixteen") == 6
    assert get_last_digit("1twone") == 1


def test_get_spelled_digit():
    assert get_spelled_digit("") is None
    assert get_spelled_digit("foo") is None
    assert get_spelled_digit("one") == 1
    assert get_spelled_digit("atwo") == 2
    assert get_spelled_digit("abthree") == 3
    assert get_spelled_digit("foura") == 4
    assert get_spelled_digit("fiveab") == 5
    assert get_spelled_digit("asixb") == 6
    assert get_spelled_digit("seveneight") == 7
    assert get_spelled_digit("eight") == 8
    assert get_spelled_digit("nineight") == 9


def test_get_spelled_digit_reversed():
    assert get_spelled_digit("one", go_backward=True) == 1
    assert get_spelled_digit("atwo", go_backward=True) == 2
    assert get_spelled_digit("threefoo", go_backward=True) == 3
    assert get_spelled_digit("twoone", go_backward=True) == 1
