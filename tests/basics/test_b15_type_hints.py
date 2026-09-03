"""B15 · 타입 힌트 채점.

런타임 동작과 **힌트 자체**를 함께 봅니다.
진짜 타입 검사는 `./study types` (mypy) 가 합니다.
"""

import typing

import pytest

from basics.b15_type_hints import (
    count_lengths,
    describe_all,
    first_or_none,
    parse_pair,
    repeat,
    safe_len,
    to_int,
)


def hints(func) -> dict:
    """문자열로 저장된 힌트를 실제 타입으로 풀어서 돌려준다."""
    return typing.get_type_hints(func)


class TestRepeat:
    def test_default(self):
        assert repeat("ab") == "abab"

    def test_custom_times(self):
        assert repeat("ab", 3) == "ababab"

    def test_zero(self):
        assert repeat("ab", 0) == ""

    def test_signature_is_annotated(self):
        annotated = hints(repeat)
        assert annotated["text"] is str
        assert annotated["times"] is int
        assert annotated["return"] is str

    def test_hints_do_nothing_at_runtime(self):
        # 힌트는 str 이라고 적혀 있지만 파이썬은 막지 않는다.
        # 리스트도 * 연산이 되므로 그냥 동작한다 — 이게 요점입니다.
        assert repeat([1], 2) == [1, 1]


class TestFirstOrNone:
    def test_first(self):
        assert first_or_none([1, 2]) == 1

    def test_empty_is_none(self):
        assert first_or_none([]) is None

    def test_return_type_allows_none(self):
        assert hints(first_or_none)["return"] == (int | None)


class TestCountLengths:
    def test_maps(self):
        assert count_lengths(["a", "bcd"]) == {"a": 1, "bcd": 3}

    def test_empty(self):
        assert count_lengths([]) == {}

    def test_return_type_says_what_is_inside(self):
        assert hints(count_lengths)["return"] == dict[str, int]


class TestParsePair:
    def test_parses(self):
        assert parse_pair("age:30") == ("age", 30)

    @pytest.mark.parametrize("bad", ["age", "", "age:삼십"])
    def test_bad_input_raises(self, bad):
        with pytest.raises(ValueError):
            parse_pair(bad)

    def test_return_type_is_a_fixed_pair(self):
        assert hints(parse_pair)["return"] == tuple[str, int]


class TestToInt:
    @pytest.mark.parametrize("value,expected", [
        ("42", 42), ("-7", -7), (3.9, 3), (-3.9, -3), (True, 1), (False, 0),
    ])
    def test_converts(self, value, expected):
        assert to_int(value) == expected

    def test_float_truncates_toward_zero(self):
        assert to_int(3.9) == 3        # 반올림이 아니라 버림

    def test_bad_string_raises(self):
        with pytest.raises(ValueError):
            to_int("abc")


class TestDescribeAll:
    def test_describes_each(self):
        assert describe_all([1, "a", 1.5]) == ["int:1", "str:a", "float:1.5"]

    def test_bool_is_not_reported_as_int(self):
        # isinstance(True, int) 는 True 라 isinstance 로 갈라내면 틀린다
        assert describe_all([True]) == ["bool:True"]

    def test_none(self):
        assert describe_all([None]) == ["NoneType:None"]

    def test_empty(self):
        assert describe_all([]) == []


class TestSafeLen:
    @pytest.mark.parametrize("value,expected", [
        ("abc", 3), ([1, 2], 2), ({"a": 1}, 1), (None, 0), ("", 0), ([], 0),
    ])
    def test_len(self, value, expected):
        assert safe_len(value) == expected
