"""B5 · 함수 채점."""

import pytest

from basics.b05_functions import apply_discount, average, multiply, to_fahrenheit, welcome


def test_multiply():
    assert multiply(3, 4) == 12


class TestWelcome:
    def test_returns_the_string(self):
        assert welcome("김파이") == "환영합니다, 김파이님"

    def test_returns_instead_of_printing(self, capsys):
        welcome("김파이")
        assert capsys.readouterr().out == ""      # print 로 짜면 여기서 걸린다


@pytest.mark.parametrize("celsius,fahrenheit", [(100, 212.0), (0, 32.0), (-40, -40.0)])
def test_to_fahrenheit(celsius, fahrenheit):
    assert to_fahrenheit(celsius) == pytest.approx(fahrenheit)


class TestAverage:
    def test_average(self):
        assert average([90, 80, 100]) == pytest.approx(90.0)

    def test_empty_raises_value_error_not_zero_division(self):
        with pytest.raises(ValueError):
            average([])


class TestApplyDiscount:
    def test_default_rate_is_10_percent(self):
        assert apply_discount(10_000) == 9_000

    def test_custom_rate(self):
        assert apply_discount(10_000, 0.25) == 7_500
