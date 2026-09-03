"""B11 · None 과 예외 채점."""

import pytest

from basics.b11_none_errors import (
    display_name,
    divide_with_log,
    find_user,
    parse_scores,
    require_positive,
    safe_divide,
    safe_int,
)

USERS = [{"name": "김", "age": 30}, {"name": "이", "age": 25}]


class TestFindUser:
    def test_finds(self):
        assert find_user(USERS, "이") == {"name": "이", "age": 25}

    def test_returns_none_when_missing(self):
        assert find_user(USERS, "최") is None

    def test_empty_list(self):
        assert find_user([], "김") is None


class TestDisplayName:
    def test_name(self):
        assert display_name({"name": "김"}) == "김"

    def test_guest_when_none(self):
        assert display_name(None) == "손님"


class TestSafeInt:
    def test_parses(self):
        assert safe_int("42") == 42

    @pytest.mark.parametrize("text", ["숫자아님", "", "3.5", "1_2_"])
    def test_falls_back_on_bad_input(self, text):
        assert safe_int(text) == 0

    def test_custom_default(self):
        assert safe_int("", -1) == -1

    def test_negative_numbers_still_parse(self):
        assert safe_int("-7") == -7

    def test_does_not_swallow_unrelated_errors(self):
        # int(None) 은 TypeError — ValueError 만 잡았다면 그대로 올라와야 한다
        with pytest.raises(TypeError):
            safe_int(None)


class TestSafeDivide:
    def test_divides(self):
        assert safe_divide(10, 2) == 5.0

    def test_zero_denominator(self):
        assert safe_divide(1, 0) is None


class TestRequirePositive:
    def test_passes_through(self):
        assert require_positive(5) == 5

    @pytest.mark.parametrize("n", [0, -3])
    def test_raises(self, n):
        with pytest.raises(ValueError):
            require_positive(n)

    def test_message_contains_the_actual_value(self):
        with pytest.raises(ValueError, match="-3"):
            require_positive(-3)          # "잘못된 입력" 만 쓰면 여기서 걸린다


class TestParseScores:
    def test_skips_unparsable(self):
        assert parse_scores(["90", "abc", "80"]) == [90, 80]

    def test_all_bad(self):
        assert parse_scores(["a", "b"]) == []

    def test_empty(self):
        assert parse_scores([]) == []


class TestDivideWithLog:
    def test_success_path(self):
        log: list[str] = []
        assert divide_with_log(10, 2, log) == 5.0
        assert log == ["시도", "성공", "정리"]

    def test_failure_path(self):
        log: list[str] = []
        assert divide_with_log(1, 0, log) is None
        assert log == ["시도", "실패", "정리"]

    def test_finally_runs_in_both_cases(self):
        for a, b in [(10, 2), (1, 0)]:
            log: list[str] = []
            divide_with_log(a, b, log)
            assert log[-1] == "정리"
