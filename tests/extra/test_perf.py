"""확장 19 · 성능 채점."""

import time

from extra.perf import intersect, stream_word_count, top_n


class TestIntersect:
    def test_keeps_order_of_a_and_removes_duplicates(self):
        assert intersect([3, 1, 2, 1], [1, 3]) == [3, 1]

    def test_empty(self):
        assert intersect([], [1, 2]) == []
        assert intersect([1, 2], []) == []

    def test_is_not_quadratic(self):
        a = list(range(100_000))
        b = list(range(50_000, 150_000))
        started = time.perf_counter()
        result = intersect(a, b)
        elapsed = time.perf_counter() - started
        assert len(result) == 50_000
        assert elapsed < 1.0        # `x in b` 로 리스트를 스캔하면 여기서 걸린다


class TestTopN:
    def test_descending(self):
        assert top_n([5, 1, 9, 3], 2) == [9, 5]

    def test_key(self):
        assert top_n(["aaa", "b", "cc"], 2, key=len) == ["aaa", "cc"]

    def test_n_is_zero_or_negative(self):
        assert top_n([1, 2, 3], 0) == []
        assert top_n([1, 2, 3], -1) == []

    def test_n_larger_than_input(self):
        assert top_n([1, 2], 10) == [2, 1]

    def test_works_on_a_generator(self):
        assert top_n((i * i for i in range(10)), 3) == [81, 64, 49]


class TestStreamWordCount:
    def test_counts_words_case_insensitively(self, tmp_path):
        path = tmp_path / "words.txt"
        path.write_text("Apple banana apple\nBANANA cherry\n", encoding="utf-8")
        counts = stream_word_count(str(path))
        assert counts["apple"] == 2
        assert counts["banana"] == 2
        assert counts["cherry"] == 1

    def test_empty_file(self, tmp_path):
        path = tmp_path / "empty.txt"
        path.write_text("", encoding="utf-8")
        assert stream_word_count(str(path)) == {}

    def test_most_common(self, tmp_path):
        path = tmp_path / "many.txt"
        path.write_text("\n".join(["a b c"] * 100 + ["a"] * 50), encoding="utf-8")
        assert stream_word_count(str(path)).most_common(1) == [("a", 150)]
