"""확장 13 모범답안."""

from __future__ import annotations

import functools
from collections.abc import Callable, Iterator
from typing import Any


def retry_collecting(
    times: int = 3,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            errors: list[Exception] = []
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    errors.append(exc)
            raise ExceptionGroup(f"{times}번 시도 모두 실패", errors)

        return wrapper

    return decorator


def numbers_with_cleanup(log: list[str]) -> Iterator[int]:
    n = 0
    try:
        while True:
            yield n
            n += 1
    finally:
        log.append("closed")


def describe_chain(exc: BaseException) -> list[str]:
    names: list[str] = []
    current: BaseException | None = exc
    while current is not None:
        names.append(type(current).__name__)
        if current.__cause__ is not None:
            current = current.__cause__
        elif current.__context__ is not None and not current.__suppress_context__:
            current = current.__context__
        else:
            current = None
    return names
