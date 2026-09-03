"""확장 17 — 동시성   (docs/26_core_17.md DRILL 17)"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
from typing import Any


async def gather_limited(
    factories: Sequence[Callable[[], Awaitable[Any]]],
    limit: int,
) -> list[Any]:
    """코루틴들을 동시에 최대 limit 개까지만 돌리고, 결과를 **입력 순서대로** 모은다.

    factories 는 "부르면 코루틴을 만들어 주는 함수"들의 리스트입니다.
    코루틴 객체를 미리 만들어 넘기지 않는 이유: 만들어 두고 실행을 미루면
    "코루틴이 await 되지 않았다" 경고가 나기 쉽고, 재시도할 때 재사용도 안 됩니다.

    asyncio.Semaphore(limit) 로 감싸고 asyncio.gather 로 모으세요.
    테스트는 '동시에 돌아간 최대 개수'를 세서 limit 을 넘지 않는지 확인합니다.
    """
    raise NotImplementedError


async def retry_async(
    factory: Callable[[], Awaitable[Any]],
    tries: int = 3,
    *,
    base_delay: float = 0.5,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> Any:
    """실패하면 지수 백오프로 다시 시도한다. tries 는 총 시도 횟수.

    대기 시간은 base_delay * 2**(시도횟수-1) — 0.5, 1.0, 2.0 ...
    마지막 시도까지 실패하면 그 예외를 그대로 올립니다.
    **마지막 실패 뒤에는 자지 않습니다** (아무도 안 기다리는데 자면 손해죠).

    sleep 을 주입받는 이유는 rate_limit 의 clock 과 같습니다 — 테스트가
    실제로 3.5초를 기다리지 않아도 되게 하려고요.
    """
    raise NotImplementedError


async def first_success(
    factories: Sequence[Callable[[], Awaitable[Any]]],
) -> Any:
    """여러 소스에 동시에 물어보고 **가장 먼저 성공한** 결과를 돌려준다.

    나머지 작업은 반드시 취소하세요. 안 그러면 이미 필요 없어진 요청이
    백그라운드에서 계속 돌면서 로그와 커넥션을 잡아먹습니다.
    전부 실패하면 ExceptionGroup 을 던집니다.
    힌트: asyncio.wait(..., return_when=FIRST_COMPLETED)
    """
    raise NotImplementedError
