"""확장 09 모범답안."""

from __future__ import annotations

import functools
import inspect
import time
from collections import deque
from collections.abc import Callable
from typing import Any

AUDIT_LOG: list[dict[str, Any]] = []
TIMINGS: dict[str, float] = {}
SENSITIVE = frozenset({"password", "token", "secret"})
MASK = "***"


def audit(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        masked = {k: (MASK if k in SENSITIVE else v) for k, v in kwargs.items()}
        record: dict[str, Any] = {"name": func.__name__, "args": args, "kwargs": masked}
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            record["error"] = type(exc).__name__
            AUDIT_LOG.append(record)
            raise
        record["result"] = result
        AUDIT_LOG.append(record)
        return result

    return wrapper


class RateLimitError(Exception):
    """허용된 호출 횟수를 넘었을 때."""


def rate_limit(
    calls: int,
    per_seconds: float,
    *,
    clock: Callable[[], float] = time.monotonic,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        history: deque[float] = deque()

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = clock()
            while history and now - history[0] >= per_seconds:
                history.popleft()
            if len(history) >= calls:
                raise RateLimitError(f"{per_seconds}초에 {calls}번까지만 허용됩니다")
            history.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def timed(func: Callable) -> Callable:
    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            started = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                TIMINGS[func.__name__] = time.perf_counter() - started

        return async_wrapper

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        started = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            TIMINGS[func.__name__] = time.perf_counter() - started

    return wrapper
