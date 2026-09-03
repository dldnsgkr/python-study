"""코어 01~05 채점."""

from decimal import Decimal

import pytest

from kit.objects import diff, flatten, group_by, rotate, split_once, total_with_vat, with_key


class TestWithKey:
    def test_returns_new_dict_without_touching_original(self):
        original = {"user": {"name": "kim", "age": 30}, "active": True}
        result = with_key(original, ["user", "name"], "lee")
        assert result["user"]["name"] == "lee"
        assert original["user"]["name"] == "kim"
        assert result["user"] is not original["user"]

    def test_creates_missing_intermediate_keys(self):
        assert with_key({}, ["a", "b"], 1) == {"a": {"b": 1}}

    def test_single_element_path(self):
        assert with_key({"a": 1}, ["a"], 2) == {"a": 2}


class TestTotalWithVat:
    @pytest.mark.parametrize("price,qty,expected", [
        ("19.99", 3, Decimal("66")),      # 59.97 * 1.1 = 65.967 → 66
        ("1000", 1, Decimal("1100")),
        ("0.05", 10, Decimal("1")),       # 0.5 * 1.1 = 0.55 → 1 (HALF_UP)
    ])
    def test_rounds_half_up(self, price, qty, expected):
        assert total_with_vat(price, qty) == expected

    def test_returns_decimal_not_float(self):
        assert isinstance(total_with_vat("100", 1), Decimal)


class TestSplitOnce:
    def test_splits_on_first_separator_only(self):
        assert split_once("key=value=extra") == ("key", "value=extra")

    def test_missing_separator(self):
        assert split_once("keyonly") == ("keyonly", "")

    def test_custom_separator(self):
        assert split_once("a:b:c", ":") == ("a", "b:c")


class TestRotate:
    @pytest.mark.parametrize("xs,k,expected", [
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
        ([1, 2, 3], 0, [1, 2, 3]),
        ([1, 2, 3], 3, [1, 2, 3]),
        ([1, 2, 3], 7, [3, 1, 2]),
        ([], 3, []),
    ])
    def test_rotate(self, xs, k, expected):
        assert rotate(xs, k) == expected

    def test_does_not_mutate_input(self):
        xs = [1, 2, 3]
        rotate(xs, 1)
        assert xs == [1, 2, 3]


class TestFlatten:
    def test_nested(self):
        assert flatten([1, [2, [3, [4]]], (5, 6)]) == [1, 2, 3, 4, 5, 6]

    def test_strings_are_not_exploded(self):
        assert flatten(["ab", ["cd"]]) == ["ab", "cd"]

    def test_empty(self):
        assert flatten([]) == []


class TestGroupBy:
    def test_groups_by_key(self):
        rows = [{"t": "a", "v": 1}, {"t": "b", "v": 2}, {"t": "a", "v": 3}]
        result = group_by(rows, lambda r: r["t"])
        assert set(result) == {"a", "b"}
        assert [r["v"] for r in result["a"]] == [1, 3]

    def test_returns_plain_dict_without_phantom_keys(self):
        result = group_by([], lambda r: r)
        assert result == {}
        result.get("missing")
        assert result == {}          # defaultdict를 그대로 반환하면 실패한다


class TestDiff:
    def test_added_removed_changed(self):
        old = {"a": 1, "b": 2, "c": 3}
        new = {"b": 2, "c": 30, "d": 4}
        result = diff(old, new)
        assert result["added"] == {"d": 4}
        assert result["removed"] == {"a": 1}
        assert result["changed"] == {"c": (3, 30)}

    def test_no_changes(self):
        result = diff({"a": 1}, {"a": 1})
        assert result == {"added": {}, "removed": {}, "changed": {}}
