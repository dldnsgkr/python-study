"""확장 09 · 데코레이터 채점."""

import pytest

from extra.decorators import AUDIT_LOG, TIMINGS, RateLimitError, audit, rate_limit, timed


@pytest.fixture(autouse=True)
def _clean_module_state():
    AUDIT_LOG.clear()
    TIMINGS.clear()
    yield
    AUDIT_LOG.clear()
    TIMINGS.clear()


class FakeClock:
    """테스트가 실제로 기다리지 않게 해 주는 가짜 시계."""

    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class TestAudit:
    def test_records_call_and_result(self):
        @audit
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        assert len(AUDIT_LOG) == 1
        assert AUDIT_LOG[0]["name"] == "add"
        assert AUDIT_LOG[0]["args"] == (1, 2)
        assert AUDIT_LOG[0]["result"] == 3

    def test_masks_sensitive_keywords(self):
        @audit
        def login(user, *, password, token, remember=False):
            return "ok"

        login("kim", password="hunter2", token="abc123", remember=True)
        kwargs = AUDIT_LOG[0]["kwargs"]
        assert kwargs["password"] == "***"
        assert kwargs["token"] == "***"
        assert kwargs["remember"] is True       # 민감하지 않은 것까지 가리면 안 된다

    def test_secret_is_never_written_anywhere(self):
        @audit
        def login(*, password):
            return "ok"

        login(password="hunter2")
        assert "hunter2" not in repr(AUDIT_LOG)

    def test_records_errors_and_reraises(self):
        @audit
        def boom():
            raise KeyError("없음")

        with pytest.raises(KeyError):
            boom()
        assert AUDIT_LOG[0]["error"] == "KeyError"

    def test_preserves_metadata(self):
        @audit
        def documented():
            """원본 docstring."""

        assert documented.__name__ == "documented"
        assert documented.__doc__ == "원본 docstring."


class TestRateLimit:
    def test_allows_up_to_the_limit(self):
        clock = FakeClock()

        @rate_limit(2, 1.0, clock=clock)
        def ping():
            return "pong"

        assert ping() == "pong"
        assert ping() == "pong"
        with pytest.raises(RateLimitError):
            ping()

    def test_window_slides(self):
        clock = FakeClock()

        @rate_limit(2, 1.0, clock=clock)
        def ping():
            return "pong"

        ping()
        ping()
        clock.advance(1.0)
        assert ping() == "pong"          # 창 밖으로 나간 기록은 버려져야 한다

    def test_partial_window(self):
        clock = FakeClock()

        @rate_limit(2, 10.0, clock=clock)
        def ping():
            return "pong"

        ping()
        clock.advance(5.0)
        ping()
        with pytest.raises(RateLimitError):
            ping()
        clock.advance(5.0)               # 첫 호출만 창 밖으로 나간다
        assert ping() == "pong"

    def test_each_decorated_function_has_its_own_budget(self):
        clock = FakeClock()

        @rate_limit(1, 1.0, clock=clock)
        def a():
            return "a"

        @rate_limit(1, 1.0, clock=clock)
        def b():
            return "b"

        assert a() == "a"
        assert b() == "b"


class TestTimed:
    def test_sync_function(self):
        @timed
        def work():
            return 42

        assert work() == 42
        assert "work" in TIMINGS
        assert TIMINGS["work"] >= 0

    def test_records_even_on_failure(self):
        @timed
        def boom():
            raise ValueError("실패")

        with pytest.raises(ValueError):
            boom()
        assert "boom" in TIMINGS

    async def test_async_function_actually_runs(self):
        @timed
        async def awork():
            return 42

        result = await awork()
        assert result == 42              # 코루틴 객체가 돌아오면 여기서 걸린다
        assert "awork" in TIMINGS

    def test_preserves_metadata(self):
        @timed
        def documented():
            """원본 docstring."""

        assert documented.__name__ == "documented"
        assert documented.__doc__ == "원본 docstring."
