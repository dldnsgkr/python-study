"""B9 · 도구상자 채점."""

from basics.b09_toolbox import (
    count_words,
    flatten_once,
    has_duplicate,
    invert,
    numbered,
    pair_up,
    rank_names,
    remove_all,
    top_two,
)

STUDENTS = [
    {"name": "김", "score": 80},
    {"name": "이", "score": 95},
    {"name": "박", "score": 95},
]


class TestNumbered:
    def test_starts_at_one(self):
        assert numbered(["사과", "배"]) == ["1. 사과", "2. 배"]

    def test_empty(self):
        assert numbered([]) == []


class TestPairUp:
    def test_zips_into_a_dict(self):
        assert pair_up(["김", "이"], [90, 80]) == {"김": 90, "이": 80}

    def test_uneven_lengths_stop_at_the_shorter(self):
        assert pair_up(["김", "이", "박"], [90]) == {"김": 90}


class TestInvert:
    def test_swaps_keys_and_values(self):
        assert invert({"김": 90, "이": 80}) == {90: "김", 80: "이"}

    def test_empty(self):
        assert invert({}) == {}


class TestCountWords:
    def test_counts(self):
        assert count_words("a b a") == {"a": 2, "b": 1}

    def test_case_insensitive(self):
        assert count_words("Python python") == {"python": 2}

    def test_empty(self):
        assert count_words("") == {}


class TestTopTwo:
    def test_descending(self):
        assert top_two([70, 95, 80]) == [95, 80]

    def test_fewer_than_two(self):
        assert top_two([10]) == [10]
        assert top_two([]) == []

    def test_does_not_mutate_the_original(self):
        scores = [70, 95, 80]
        top_two(scores)
        assert scores == [70, 95, 80]     # .sort() 를 쓰면 여기서 걸린다


class TestRankNames:
    def test_highest_first(self):
        assert rank_names(STUDENTS) == ["이", "박", "김"]

    def test_ties_keep_original_order(self):
        assert rank_names(STUDENTS)[:2] == ["이", "박"]   # 정렬은 안정적이다

    def test_empty(self):
        assert rank_names([]) == []


class TestRemoveAll:
    def test_removes_every_occurrence(self):
        assert remove_all([1, 2, 1, 3], 1) == [2, 3]

    def test_does_not_mutate_the_original(self):
        xs = [1, 2, 1]
        remove_all(xs, 1)
        assert xs == [1, 2, 1]

    def test_value_not_present(self):
        assert remove_all([1, 2], 9) == [1, 2]


class TestFlattenOnce:
    def test_flattens(self):
        assert flatten_once([[1, 2], [3], []]) == [1, 2, 3]

    def test_only_one_level(self):
        assert flatten_once([[1, [2]], [3]]) == [1, [2], 3]

    def test_empty(self):
        assert flatten_once([]) == []


class TestHasDuplicate:
    def test_true(self):
        assert has_duplicate([1, 2, 1]) is True

    def test_false(self):
        assert has_duplicate([1, 2, 3]) is False

    def test_empty(self):
        assert has_duplicate([]) is False
