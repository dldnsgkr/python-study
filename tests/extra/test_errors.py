"""확장 13 · 예외 채점."""

import gc

import pytest

from extra.errors import describe_chain, numbers_with_cleanup, retry_collecting


class TestRetryCollecting:
    def test_returns_on_success_without_retrying(self):
        calls = []

        @retry_collecting(times=3)
        def ok():
            calls.append(1)
            return "ok"

        assert ok() == "ok"
        assert len(calls) == 1

    def test_collects_every_attempt_into_one_group(self):
        raised = [ValueError("타임아웃"), KeyError("인증"), ValueError("404")]
        calls = []

        @retry_collecting(times=3, exceptions=(ValueError, KeyError))
        def flaky():
            exc = raised[len(calls)]
            calls.append(1)
            raise exc

        with pytest.raises(ExceptionGroup) as info:
            flaky()
        assert len(info.value.exceptions) == 3
        matched, _ = info.value.split(ValueError)
        assert len(matched.exceptions) == 2      # 마지막 예외만 남기면 실패한다

    def test_can_be_caught_with_except_star(self):
        @retry_collecting(times=2, exceptions=(ValueError,))
        def flaky():
            raise ValueError("실패")

        caught = []
        try:
            flaky()
        except* ValueError as group:
            caught.extend(group.exceptions)
        assert len(caught) == 2

    def test_does_not_swallow_other_exceptions(self):
        @retry_collecting(times=3, exceptions=(ValueError,))
        def wrong():
            raise KeyError("다른 예외")

        with pytest.raises(KeyError):
            wrong()


class TestNumbersWithCleanup:
    def test_yields_numbers(self):
        log: list[str] = []
        gen = numbers_with_cleanup(log)
        assert [next(gen), next(gen), next(gen)] == [0, 1, 2]
        assert log == []                  # 아직 정리되지 않았다

    def test_close_runs_finally(self):
        log: list[str] = []
        gen = numbers_with_cleanup(log)
        next(gen)
        gen.close()
        assert log == ["closed"]

    def test_break_then_drop_runs_finally(self):
        log: list[str] = []

        def consume():
            for n in numbers_with_cleanup(log):
                if n == 2:
                    break

        consume()
        gc.collect()
        assert log == ["closed"]


class TestDescribeChain:
    def test_explicit_cause(self):
        try:
            try:
                raise FileNotFoundError("없음")
            except FileNotFoundError as exc:
                raise ValueError("변환") from exc
        except ValueError as exc:
            assert describe_chain(exc) == ["ValueError", "FileNotFoundError"]

    def test_implicit_context(self):
        try:
            try:
                raise KeyError("k")
            except KeyError:
                raise RuntimeError("처리 중")
        except RuntimeError as exc:
            assert describe_chain(exc) == ["RuntimeError", "KeyError"]

    def test_from_none_hides_the_context(self):
        try:
            try:
                raise KeyError("k")
            except KeyError:
                raise RuntimeError("숨김") from None
        except RuntimeError as exc:
            assert describe_chain(exc) == ["RuntimeError"]

    def test_standalone_exception(self):
        assert describe_chain(ValueError("혼자")) == ["ValueError"]
