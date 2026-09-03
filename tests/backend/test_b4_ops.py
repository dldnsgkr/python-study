"""B4 · 운영 채점."""

import asyncio
import io
import json
import logging

import pytest

pytest.importorskip("fastapi", reason="uv sync --group backend 를 먼저 실행하세요")

from fastapi import FastAPI  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402

from backend.b4_ops import (  # noqa: E402
    GracefulShutdown,
    JsonFormatter,
    ShuttingDownError,
    add_timing_middleware,
    build_logger,
    get_trace_id,
    new_trace_id,
    set_trace_id,
    trace_id_var,
)


@pytest.fixture
def log_stream():
    return io.StringIO()


@pytest.fixture
def logger(log_stream, request):
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(JsonFormatter())
    return build_logger(f"test.{request.node.name}", handler)


@pytest.fixture(autouse=True)
def _reset_trace_id():
    token = trace_id_var.set(None)
    yield
    trace_id_var.reset(token)


def records(stream: io.StringIO) -> list[dict]:
    return [json.loads(line) for line in stream.getvalue().splitlines() if line.strip()]


class TestTraceId:
    def test_starts_empty(self):
        assert get_trace_id() is None

    def test_set_and_get(self):
        set_trace_id("abc123")
        assert get_trace_id() == "abc123"

    def test_new_trace_id_is_a_32_char_hex(self):
        value = new_trace_id()
        assert len(value) == 32
        int(value, 16)                       # 16진수가 아니면 여기서 터진다

    def test_ids_are_unique(self):
        assert len({new_trace_id() for _ in range(100)}) == 100

    async def test_survives_await_boundaries(self):
        set_trace_id("across-await")

        async def nested():
            await asyncio.sleep(0)
            return get_trace_id()

        assert await nested() == "across-await"   # 스레드로컬과 달리 async 를 넘어간다

    async def test_tasks_get_their_own_copy(self):
        set_trace_id("parent")

        async def child():
            set_trace_id("child")
            return get_trace_id()

        assert await asyncio.create_task(child()) == "child"
        assert get_trace_id() == "parent"     # 자식이 부모를 오염시키지 않는다


class TestJsonFormatter:
    def test_emits_valid_json_with_the_core_fields(self, logger, log_stream):
        logger.info("주문 생성")
        record = records(log_stream)[0]
        assert record["level"] == "INFO"
        assert record["msg"] == "주문 생성"
        assert record["ts"]
        assert record["logger"] == logger.name

    def test_applies_percent_formatting(self, logger, log_stream):
        logger.info("주문 %s 처리", 42)
        assert records(log_stream)[0]["msg"] == "주문 42 처리"   # record.msg 면 실패한다

    def test_trace_id_is_injected_when_set(self, logger, log_stream):
        set_trace_id("trace-xyz")
        logger.info("무언가")
        assert records(log_stream)[0]["trace_id"] == "trace-xyz"

    def test_trace_id_key_is_absent_when_unset(self, logger, log_stream):
        logger.info("무언가")
        assert "trace_id" not in records(log_stream)[0]

    def test_extra_fields_are_flattened_to_the_top_level(self, logger, log_stream):
        logger.info("주문 생성", extra={"extra_fields": {"order_id": 1, "channel": "web"}})
        record = records(log_stream)[0]
        assert record["order_id"] == 1
        assert record["channel"] == "web"     # {"extra_fields": {...}} 로 중첩되면 실패

    def test_exception_is_captured(self, logger, log_stream):
        try:
            raise ValueError("터짐")
        except ValueError:
            logger.exception("실패")
        record = records(log_stream)[0]
        assert "ValueError" in record["exc"]

    def test_korean_is_not_escaped(self, logger, log_stream):
        logger.info("한글 메시지")
        raw = log_stream.getvalue()
        assert json.loads(raw)["msg"] == "한글 메시지"   # JSON 이어야 하고
        assert "한글 메시지" in raw                      # \uXXXX 로 깨지지 않아야 한다


class TestTimingMiddleware:
    @pytest.fixture
    def app_factory(self, logger):
        def make(slow_seconds: float = 1.0) -> FastAPI:
            app = FastAPI()

            @app.get("/ping")
            async def ping() -> dict[str, bool]:
                return {"ok": True}

            @app.get("/boom")
            async def boom() -> dict[str, bool]:
                raise ValueError("실패")

            add_timing_middleware(app, logger, slow_seconds=slow_seconds)
            return app

        return make

    async def _get(self, app, path="/ping"):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            return await c.get(path)

    async def test_logs_method_path_status_and_duration(self, app_factory, log_stream):
        await self._get(app_factory())
        record = records(log_stream)[0]
        assert record["method"] == "GET"
        assert record["path"] == "/ping"
        assert record["status"] == 200
        assert isinstance(record["duration_ms"], int | float)

    async def test_fast_request_is_info(self, app_factory, log_stream):
        await self._get(app_factory(slow_seconds=10))
        assert records(log_stream)[0]["level"] == "INFO"

    async def test_slow_request_is_warning(self, app_factory, log_stream):
        await self._get(app_factory(slow_seconds=0))    # 무엇이든 '느린' 요청이 된다
        assert records(log_stream)[0]["level"] == "WARNING"

    async def test_response_carries_the_trace_id_header(self, app_factory):
        resp = await self._get(app_factory())
        assert len(resp.headers["X-Trace-Id"]) == 32

    async def test_log_and_header_share_the_same_trace_id(self, app_factory, log_stream):
        resp = await self._get(app_factory())
        assert records(log_stream)[0]["trace_id"] == resp.headers["X-Trace-Id"]

    async def test_each_request_gets_a_fresh_trace_id(self, app_factory, log_stream):
        app = app_factory()
        await self._get(app)
        await self._get(app)
        traces = [r["trace_id"] for r in records(log_stream)]
        assert len(set(traces)) == 2


class TestGracefulShutdown:
    async def test_accepts_before_shutdown(self):
        shutdown = GracefulShutdown()
        assert shutdown.accepting is True
        async with shutdown.track_request():
            assert shutdown.in_flight == 1
        assert shutdown.in_flight == 0

    async def test_rejects_new_requests_after_shutdown_starts(self):
        shutdown = GracefulShutdown()
        shutdown.start_shutdown()
        assert shutdown.accepting is False
        with pytest.raises(ShuttingDownError):
            async with shutdown.track_request():
                pass

    async def test_counter_is_restored_even_on_error(self):
        shutdown = GracefulShutdown()
        with pytest.raises(ValueError):
            async with shutdown.track_request():
                raise ValueError("핸들러 실패")
        assert shutdown.in_flight == 0        # finally 를 빠뜨리면 영원히 종료 못 한다

    async def test_wait_idle_returns_immediately_when_idle(self):
        shutdown = GracefulShutdown()
        assert await asyncio.wait_for(shutdown.wait_idle(), timeout=0.5) is True

    async def test_wait_idle_waits_for_in_flight_requests(self):
        shutdown = GracefulShutdown()
        finished = []

        async def slow_request():
            async with shutdown.track_request():
                await asyncio.sleep(0.05)
                finished.append(True)

        task = asyncio.create_task(slow_request())
        await asyncio.sleep(0)                # 요청이 시작되게 한 틱 양보
        shutdown.start_shutdown()
        assert await shutdown.wait_idle(timeout=1.0) is True
        assert finished == [True]             # 진행 중이던 요청은 끝까지 처리됐다
        await task

    async def test_wait_idle_times_out_when_still_busy(self):
        shutdown = GracefulShutdown()

        async def never_ending():
            async with shutdown.track_request():
                await asyncio.sleep(5)

        task = asyncio.create_task(never_ending())
        await asyncio.sleep(0)
        assert await shutdown.wait_idle(timeout=0.05) is False
        task.cancel()

    async def test_concurrent_requests_are_all_tracked(self):
        shutdown = GracefulShutdown()

        async def request():
            async with shutdown.track_request():
                await asyncio.sleep(0.02)

        tasks = [asyncio.create_task(request()) for _ in range(5)]
        await asyncio.sleep(0.005)
        assert shutdown.in_flight == 5
        await asyncio.gather(*tasks)
        assert shutdown.in_flight == 0
