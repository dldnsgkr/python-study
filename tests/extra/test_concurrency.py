"""확장 17 · 동시성 채점."""

import asyncio
from functools import partial

import pytest

from extra.concurrency import first_success, gather_limited, retry_async


class TestGatherLimited:
    async def test_results_keep_input_order(self):
        async def work(i):
            await asyncio.sleep(0.01 * (5 - i))     # 늦게 끝나는 것이 먼저 들어온다
            return i

        result = await gather_limited([partial(work, i) for i in range(5)], 5)
        assert result == [0, 1, 2, 3, 4]

    async def test_never_exceeds_the_limit(self):
        active = 0
        peak = 0

        async def work(i):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.01)
            active -= 1
            return i

        await gather_limited([partial(work, i) for i in range(12)], 3)
        assert peak <= 3

    async def test_actually_runs_concurrently(self):
        active = 0
        peak = 0

        async def work():
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.02)
            active -= 1

        await gather_limited([work] * 6, 3)
        assert peak == 3        # 1 이면 순차 실행 — 세마포어 없이 그냥 await 한 것


class TestRetryAsync:
    async def test_succeeds_and_records_backoff(self):
        delays = []

        async def fake_sleep(seconds):
            delays.append(seconds)

        calls = []

        async def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise ValueError("아직")
            return "ok"

        result = await retry_async(flaky, tries=3, base_delay=0.5, sleep=fake_sleep)
        assert result == "ok"
        assert delays == [0.5, 1.0]      # 지수 백오프

    async def test_does_not_sleep_after_the_last_failure(self):
        delays = []

        async def fake_sleep(seconds):
            delays.append(seconds)

        async def always_fails():
            raise ValueError("끝까지 실패")

        with pytest.raises(ValueError, match="끝까지"):
            await retry_async(always_fails, tries=3, sleep=fake_sleep)
        assert delays == [0.5, 1.0]      # 3번째 실패 뒤엔 자지 않는다

    async def test_single_try(self):
        delays = []

        async def fake_sleep(seconds):
            delays.append(seconds)

        async def always_fails():
            raise ValueError("실패")

        with pytest.raises(ValueError):
            await retry_async(always_fails, tries=1, sleep=fake_sleep)
        assert delays == []


class TestFirstSuccess:
    async def test_returns_the_fastest_and_cancels_the_rest(self):
        cancelled = []

        async def slow(name):
            try:
                await asyncio.sleep(5)
                return name
            except asyncio.CancelledError:
                cancelled.append(name)
                raise

        async def fast():
            await asyncio.sleep(0.01)
            return "fast"

        result = await first_success([partial(slow, "a"), fast, partial(slow, "b")])
        assert result == "fast"
        assert sorted(cancelled) == ["a", "b"]   # 남은 작업을 안 끊으면 계속 돈다

    async def test_skips_failures(self):
        async def boom():
            raise ValueError("실패")

        async def ok():
            await asyncio.sleep(0.01)
            return "ok"

        assert await first_success([boom, ok]) == "ok"

    async def test_all_failed_raises_exception_group(self):
        async def boom(msg):
            raise ValueError(msg)

        with pytest.raises(ExceptionGroup) as info:
            await first_success([partial(boom, "a"), partial(boom, "b")])
        assert len(info.value.exceptions) == 2
