"""B4 모범답안."""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from contextvars import ContextVar

from fastapi import FastAPI


def build_logger(name: str, handler: logging.Handler, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger


trace_id_var: ContextVar[str | None] = ContextVar("trace_id", default=None)


def new_trace_id() -> str:
    return uuid.uuid4().hex


def set_trace_id(value: str) -> None:
    trace_id_var.set(value)


def get_trace_id() -> str | None:
    return trace_id_var.get()


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        trace_id = get_trace_id()
        if trace_id is not None:
            payload["trace_id"] = trace_id
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        payload.update(getattr(record, "extra_fields", {}))
        return json.dumps(payload, ensure_ascii=False)


def add_timing_middleware(
    app: FastAPI,
    logger: logging.Logger,
    slow_seconds: float = 1.0,
) -> None:
    @app.middleware("http")
    async def timing(request, call_next):  # noqa: ANN001, ANN202
        trace_id = new_trace_id()
        set_trace_id(trace_id)
        started = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - started

        level = logging.WARNING if elapsed > slow_seconds else logging.INFO
        logger.log(level, "request", extra={"extra_fields": {
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round(elapsed * 1000, 1),
        }})
        response.headers["X-Trace-Id"] = trace_id
        return response


class ShuttingDownError(Exception):
    """종료가 시작된 뒤 들어온 새 요청."""


class GracefulShutdown:
    def __init__(self) -> None:
        self._accepting = True
        self._in_flight = 0
        self._idle = asyncio.Event()
        self._idle.set()

    @property
    def accepting(self) -> bool:
        return self._accepting

    @property
    def in_flight(self) -> int:
        return self._in_flight

    @asynccontextmanager
    async def track_request(self) -> AsyncIterator[None]:
        if not self._accepting:
            raise ShuttingDownError("서버가 종료 중입니다")
        self._in_flight += 1
        self._idle.clear()
        try:
            yield
        finally:
            self._in_flight -= 1
            if self._in_flight == 0:
                self._idle.set()

    def start_shutdown(self) -> None:
        self._accepting = False

    async def wait_idle(self, timeout: float | None = None) -> bool:
        if timeout is None:
            await self._idle.wait()
            return True
        try:
            await asyncio.wait_for(self._idle.wait(), timeout)
        except TimeoutError:
            return False
        return True
