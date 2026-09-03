"""확장 17 모범답안."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
from typing import Any


async def gather_limited(
    factories: Sequence[Callable[[], Awaitable[Any]]],
    limit: int,
) -> list[Any]:
    semaphore = asyncio.Semaphore(limit)

    async def run(factory: Callable[[], Awaitable[Any]]) -> Any:
        async with semaphore:
            return await factory()

    return list(await asyncio.gather(*(run(f) for f in factories)))


async def retry_async(
    factory: Callable[[], Awaitable[Any]],
    tries: int = 3,
    *,
    base_delay: float = 0.5,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> Any:
    for attempt in range(1, tries + 1):
        try:
            return await factory()
        except Exception:
            if attempt == tries:
                raise
            await sleep(base_delay * 2 ** (attempt - 1))
    raise AssertionError("도달할 수 없음")


async def first_success(
    factories: Sequence[Callable[[], Awaitable[Any]]],
) -> Any:
    if not factories:
        raise ValueError("factories 가 비었습니다")

    pending: set[asyncio.Future[Any]] = {
        asyncio.ensure_future(factory()) for factory in factories
    }
    errors: list[Exception] = []
    try:
        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                exc = task.exception()
                if exc is None:
                    return task.result()
                if not isinstance(exc, Exception):
                    raise exc          # KeyboardInterrupt 같은 건 삼키지 않는다
                errors.append(exc)
    finally:
        for task in pending:
            task.cancel()
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
    raise ExceptionGroup("모든 소스가 실패했습니다", errors)
