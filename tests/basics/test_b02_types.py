"""B2 · 타입 채점."""

import pytest

from basics.b02_types import describe_type, divide_report, greet, is_even, sum_of_inputs


@pytest.mark.parametrize("value,expected", [
    (3, "int"), (3.5, "float"), ("hi", "str"), (True, "bool"), ([1], "list"),
])
def test_describe_type(value, expected):
    assert describe_type(value) == expected


def test_greet():
    assert greet("김파이", 25) == "김파이님은 25살입니다"


def test_divide_report():
    assert divide_report(17, 5) == (3.4, 3, 2)


@pytest.mark.parametrize("n,expected", [(8, True), (7, False), (0, True), (-4, True)])
def test_is_even(n, expected):
    assert is_even(n) is expected


def test_sum_of_inputs_converts_before_adding():
    assert sum_of_inputs("3", "5") == 8          # "35" 가 나오면 변환을 빠뜨린 것
    assert isinstance(sum_of_inputs("1", "2"), int)
