"""확장 08 · 이터레이션 채점."""

from itertools import count, islice, takewhile

from extra.iteration import fib, jsonl_batches, parse_jsonl, unique_everseen


class TestFib:
    def test_first_ten(self):
        assert list(islice(fib(), 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_is_infinite_and_lazy(self):
        assert len(list(islice(fib(), 20))) == 20
        assert list(takewhile(lambda x: x < 1000, fib()))[-1] == 987

    def test_independent_generators(self):
        a, b = fib(), fib()
        next(a)
        assert next(b) == 0


class TestUniqueEverseen:
    def test_keeps_first_occurrence_order(self):
        assert list(unique_everseen("AAABBCCDA")) == ["A", "B", "C", "D"]

    def test_key_function(self):
        words = ["apple", "Apple", "banana"]
        assert list(unique_everseen(words, key=str.lower)) == ["apple", "banana"]

    def test_lazy_on_infinite_iterable(self):
        got = list(islice(unique_everseen(count()), 3))
        assert got == [0, 1, 2]      # 전부 모았다가 반환하면 여기서 멈추지 않는다


class TestParseJsonl:
    def test_parses_and_skips_blank_lines(self):
        lines = ['{"a": 1}', "", "   ", '{"a": 2}']
        assert list(parse_jsonl(lines)) == [{"a": 1}, {"a": 2}]

    def test_broken_line_propagates(self):
        import pytest
        with pytest.raises(ValueError):
            list(parse_jsonl(["{broken"]))


class TestJsonlBatches:
    def test_filters_then_batches(self):
        lines = [f'{{"n": {i}}}' for i in range(10)]
        got = list(jsonl_batches(lines, lambda r: r["n"] % 2 == 0, 2))
        assert got == [
            [{"n": 0}, {"n": 2}],
            [{"n": 4}, {"n": 6}],
            [{"n": 8}],
        ]

    def test_no_match_yields_nothing(self):
        lines = ['{"n": 1}']
        assert list(jsonl_batches(lines, lambda r: False, 3)) == []

    def test_is_lazy_all_the_way_down(self):
        consumed = []

        def source():
            for i in count():
                consumed.append(i)
                yield f'{{"n": {i}}}'

        first = next(jsonl_batches(source(), lambda r: True, 2))
        assert first == [{"n": 0}, {"n": 1}]
        assert len(consumed) <= 3        # 소스를 통째로 읽으면 무한 루프거나 값이 커진다
