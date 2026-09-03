"""확장 05 · 매핑 채점."""

import pytest

from extra.mappings import LRUCache, merge_deep


class TestLRUCache:
    def test_basic_get_put(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        assert cache.get("a") == 1
        assert cache.get("zzz") is None
        assert cache.get("zzz", "기본값") == "기본값"

    def test_evicts_the_least_recently_used(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")            # a 를 최근 사용으로 끌어올린다
        cache.put("c", 3)         # 이제 밀려나는 건 b
        assert cache.get("b") is None
        assert cache.get("a") == 1
        assert cache.get("c") == 3

    def test_keys_are_oldest_to_newest(self):
        cache = LRUCache(3)
        for key, value in [("a", 1), ("b", 2), ("c", 3)]:
            cache.put(key, value)
        assert cache.keys() == ["a", "b", "c"]
        cache.get("a")
        assert cache.keys() == ["b", "c", "a"]

    def test_updating_existing_key_refreshes_position(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 10)
        cache.put("c", 3)
        assert cache.get("b") is None      # a 가 아니라 b 가 밀려나야 한다
        assert cache.get("a") == 10

    def test_len_never_exceeds_capacity(self):
        cache = LRUCache(2)
        for i in range(10):
            cache.put(i, i)
        assert len(cache) == 2

    def test_rejects_non_positive_capacity(self):
        with pytest.raises(ValueError):
            LRUCache(0)


class TestMergeDeep:
    def test_nested_override(self):
        base = {"a": {"x": 1, "y": 2}, "b": 1}
        override = {"a": {"y": 9}, "c": 3}
        assert merge_deep(base, override) == {"a": {"x": 1, "y": 9}, "b": 1, "c": 3}

    def test_non_dict_wins(self):
        assert merge_deep({"a": {"x": 1}}, {"a": 5}) == {"a": 5}
        assert merge_deep({"a": 5}, {"a": {"x": 1}}) == {"a": {"x": 1}}

    def test_originals_are_untouched(self):
        base = {"a": {"x": 1}}
        override = {"a": {"y": 2}}
        result = merge_deep(base, override)
        result["a"]["x"] = 999
        assert base == {"a": {"x": 1}}
        assert override == {"a": {"y": 2}}

    def test_empty(self):
        assert merge_deep({}, {}) == {}
        assert merge_deep({"a": 1}, {}) == {"a": 1}
