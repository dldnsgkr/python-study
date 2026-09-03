"""B4 · 흐름 제어 채점."""

import pytest

from basics.b04_flow import bigger_than, grade, sign, sum_to, times_table


@pytest.mark.parametrize("n,expected", [(5, "양수"), (-5, "음수"), (0, "0")])
def test_sign(n, expected):
    assert sign(n) == expected


class TestTimesTable:
    def test_two(self):
        rows = times_table(2)
        assert len(rows) == 9
        assert rows[0] == "2 x 1 = 2"
        assert rows[8] == "2 x 9 = 18"

    def test_seven(self):
        assert times_table(7)[6] == "7 x 7 = 49"


@pytest.mark.parametrize("n,expected", [(100, 5050), (1, 1), (0, 0), (-3, 0)])
def test_sum_to(n, expected):
    assert sum_to(n) == expected


def test_bigger_than_keeps_order():
    assert bigger_than([15, 8, 23, 4, 42], 20) == [23, 42]
    assert bigger_than([1, 2], 100) == []


class TestGrade:
    @pytest.mark.parametrize("score,expected", [
        (100, "A"), (90, "A"), (89, "B"), (80, "B"),
        (79, "C"), (70, "C"), (69, "F"), (0, "F"),
    ])
    def test_boundaries(self, score, expected):
        assert grade(score) == expected

    @pytest.mark.parametrize("score", [-1, 101, 1000])
    def test_rejects_impossible_scores(self, score):
        with pytest.raises(ValueError):
            grade(score)
