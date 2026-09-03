"""코어 06~09 채점."""

from itertools import count

import pytest

from kit.functions import batches, bind_args, first_match, make_counter, retry, transpose, window


class TestFirstMatch:
    def test_found(self):
        assert first_match([1, 3, 4, 6], lambda x: x % 2 == 0) == 4

    def test_default_when_missing(self):
        assert first_match([1, 3], lambda x: x > 100, default=-1) == -1

    def test_lazy_on_infinite_iterable(self):
        assert first_match(count(), lambda x: x > 5) == 6      # 무한 루프면 실패


class TestTranspose:
    def test_square_and_rect(self):
        assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]

    def test_empty(self):
        assert transpose([]) == []


class TestMakeCounter:
    def test_counts_up(self):
        c = make_counter()
        assert [c(), c(), c()] == [1, 2, 3]

    def test_counters_are_independent(self):
        a, b = make_counter(), make_counter(10)
        a()
        assert b() == 11


class TestBindArgs:
    def test_normalizes_positional_and_defaults(self):
        def f(a, b=2, *, c=3):
            ...
        assert bind_args(f, 1) == {"a": 1, "b": 2, "c": 3}
        assert bind_args(f, 1, 9, c=8) == {"a": 1, "b": 9, "c": 8}


class TestWindow:
    def test_sliding(self):
        assert list(window([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]

    def test_shorter_than_window(self):
        assert list(window([1], 3)) == []

    def test_yields_snapshots_not_live_buffer(self):
        got = list(window([1, 2, 3, 4], 2))
        assert got[0] == (1, 2)          # 버퍼를 그대로 yield하면 여기서 깨진다

    def test_lazy(self):
        assert next(window(count(), 3)) == (0, 1, 2)


class TestBatches:
    def test_last_batch_may_be_smaller(self):
        assert list(batches(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]]

    def test_empty(self):
        assert list(batches([], 3)) == []

    def test_size_larger_than_input(self):
        assert list(batches([1, 2], 10)) == [[1, 2]]


class TestRetry:
    def test_retries_until_success(self):
        calls = []

        @retry(times=3, exceptions=(ValueError,))
        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise ValueError("아직")
            return "ok"

        assert flaky() == "ok"
        assert len(calls) == 3

    def test_reraises_after_exhausting(self):
        @retry(times=2, exceptions=(ValueError,))
        def always_fails():
            raise ValueError("끝까지 실패")

        with pytest.raises(ValueError, match="끝까지"):
            always_fails()

    def test_times_is_total_attempts_not_extra_retries(self):
        calls = []

        @retry(times=2, exceptions=(ValueError,))
        def always_fails():
            calls.append(1)
            raise ValueError("실패")

        with pytest.raises(ValueError):
            always_fails()
        assert len(calls) == 2       # 3이 나오면 times 를 '추가 재시도'로 해석한 것

    def test_does_not_swallow_other_exceptions(self):
        @retry(times=3, exceptions=(ValueError,))
        def wrong_error():
            raise KeyError("다른 예외")

        with pytest.raises(KeyError):
            wrong_error()

    def test_preserves_metadata(self):
        @retry()
        def documented():
            """원본 docstring."""

        assert documented.__name__ == "documented"
        assert documented.__doc__ == "원본 docstring."
