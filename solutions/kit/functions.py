"""코어 06~09 모범답안."""

from __future__ import annotations

import functools
import inspect
from collections import deque
from collections.abc import Callable, Iterable, Iterator
from itertools import islice
from typing import Any


def first_match(xs: Iterable, pred: Callable[[Any], bool], default: Any = None) -> Any:
    return next((x for x in xs if pred(x)), default)


def transpose(matrix: list[list]) -> list[list]:
    return [list(row) for row in zip(*matrix, strict=True)]


def make_counter(start: int = 0) -> Callable[[], int]:
    count = start

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def bind_args(func: Callable, *args: Any, **kwargs: Any) -> dict:
    bound = inspect.signature(func).bind(*args, **kwargs)
    bound.apply_defaults()
    return dict(bound.arguments)


def window(iterable: Iterable, n: int) -> Iterator[tuple]:
    it = iter(iterable)
    buf = deque(islice(it, n), maxlen=n)
    if len(buf) == n:
        yield tuple(buf)          # 버퍼 자체가 아니라 스냅샷을 내보낸다
    for item in it:
        buf.append(item)
        yield tuple(buf)


def batches(iterable: Iterable, size: int) -> Iterator[list]:
    it = iter(iterable)
    while chunk := list(islice(it, size)):
        yield chunk


def retry(times: int = 3, exceptions: tuple[type[BaseException], ...] = (Exception,)) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
            raise AssertionError("도달할 수 없음")

        return wrapper

    return decorator
