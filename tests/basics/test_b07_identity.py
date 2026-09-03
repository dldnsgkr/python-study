"""B7 · == 와 is 채점."""

import pytest

from basics.b07_identity import alias_and_append, average_score, compare, top_student

STUDENTS = [
    {"name": "김파이", "score": 90},
    {"name": "이자바", "score": 85},
    {"name": "박씨플", "score": 78},
]


class TestCompare:
    def test_equal_values_are_not_the_same_object(self):
        assert compare([1, 2], [1, 2]) == (True, False)

    def test_same_object(self):
        xs = [1, 2]
        assert compare(xs, xs) == (True, True)

    def test_different_values(self):
        assert compare([1], [2]) == (False, False)


def test_alias_shares_the_same_object():
    xs = [1, 2]
    original, alias = alias_and_append(xs, 3)
    assert original is alias            # 복사본을 만들면 여기서 걸린다
    assert original == [1, 2, 3]
    assert xs == [1, 2, 3]              # 인자로 넘긴 리스트도 함께 바뀐다


class TestAverageScore:
    def test_average(self):
        assert average_score(STUDENTS) == pytest.approx((90 + 85 + 78) / 3)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            average_score([])


class TestTopStudent:
    def test_highest(self):
        assert top_student(STUDENTS) == "김파이"

    def test_tie_takes_the_first(self):
        tied = [{"name": "A", "score": 90}, {"name": "B", "score": 90}]
        assert top_student(tied) == "A"
