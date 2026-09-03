"""B1 · 변수 채점."""

import pytest

from basics.b01_variables import add_to_price, introduce, swap, total_seconds


def test_introduce():
    assert introduce("김파이", 25, 172.5) == "김파이님은 25살, 키는 172.5cm입니다"


def test_add_to_price():
    assert add_to_price(1000, 500) == 1500


@pytest.mark.parametrize("a,b", [(5, 3), ("x", "y"), (0, 0)])
def test_swap(a, b):
    assert swap(a, b) == (b, a)


def test_total_seconds():
    assert total_seconds(1) == 86_400
    assert total_seconds(0) == 0
    assert total_seconds(3) == 259_200
