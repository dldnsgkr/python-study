"""B10 · 반복의 도구 채점."""

import pytest

from basics.b10_loops import (
    all_pairs,
    countdown,
    every_nth,
    first_negative,
    long_words,
    skip_comments,
    squares,
    word_lengths,
)


class TestCountdown:
    def test_counts_down(self):
        assert countdown(3) == [3, 2, 1]

    @pytest.mark.parametrize("n", [0, -1])
    def test_non_positive_is_empty(self, n):
        assert countdown(n) == []

    def test_does_not_hang(self):
        assert len(countdown(1000)) == 1000     # 무한 루프면 여기서 안 끝난다


class TestFirstNegative:
    def test_finds_the_first(self):
        assert first_negative([3, -1, -5]) == -1

    def test_none_when_missing(self):
        assert first_negative([1, 2]) is None

    def test_empty(self):
        assert first_negative([]) is None

    def test_stops_early(self):
        # 뒤에 문자열이 섞여 있어도, 앞에서 찾고 멈추면 문제가 없다
        assert first_negative([-1, "터짐"]) == -1


class TestSkipComments:
    def test_drops_blanks_and_comments(self):
        assert skip_comments(["a", "", "# 주석", "  b  "]) == ["a", "b"]

    def test_whitespace_only_line_is_dropped(self):
        assert skip_comments(["   "]) == []

    def test_indented_comment_is_dropped(self):
        assert skip_comments(["   # 들여쓴 주석"]) == []

    def test_hash_inside_a_line_is_kept(self):
        assert skip_comments(["색상 #ff0000"]) == ["색상 #ff0000"]


class TestEveryNth:
    def test_steps(self):
        assert every_nth(0, 10, 3) == [0, 3, 6, 9]

    def test_end_is_exclusive(self):
        assert every_nth(0, 9, 3) == [0, 3, 6]

    def test_step_of_one(self):
        assert every_nth(1, 4, 1) == [1, 2, 3]


class TestAllPairs:
    def test_combinations(self):
        assert all_pairs(["a", "b", "c"]) == [("a", "b"), ("a", "c"), ("b", "c")]

    def test_no_self_pairs_and_no_duplicates(self):
        pairs = all_pairs(["a", "b"])
        assert pairs == [("a", "b")]        # ("b","a") 나 ("a","a") 가 있으면 실패

    def test_too_few(self):
        assert all_pairs(["a"]) == []
        assert all_pairs([]) == []


class TestSquares:
    def test_squares(self):
        assert squares([1, 2, 3]) == [1, 4, 9]

    def test_empty(self):
        assert squares([]) == []

    def test_negatives(self):
        assert squares([-2]) == [4]


class TestLongWords:
    def test_filters(self):
        assert long_words(["a", "abc", "abcd"], 3) == ["abc", "abcd"]

    def test_boundary_is_inclusive(self):
        assert long_words(["abc"], 3) == ["abc"]

    def test_none_match(self):
        assert long_words(["a"], 5) == []


class TestWordLengths:
    def test_maps_word_to_length(self):
        assert word_lengths(["a", "abc"]) == {"a": 1, "abc": 3}

    def test_empty(self):
        assert word_lengths([]) == {}
