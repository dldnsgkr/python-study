"""확장 09 — 데코레이터   (docs/18_core_09.md DRILL 09)"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

#: audit 데코레이터가 남긴 기록. 테스트가 이 리스트를 들여다봅니다.
AUDIT_LOG: list[dict[str, Any]] = []

#: timed 데코레이터가 잰 시간. {"함수이름": 초}
TIMINGS: dict[str, float] = {}

#: 민감 정보로 취급해 가릴 키워드 인자 이름
SENSITIVE = frozenset({"password", "token", "secret"})

MASK = "***"


def audit(func: Callable) -> Callable:
    """호출 인자와 반환값을 AUDIT_LOG 에 기록하되, 민감한 키워드 인자는 가린다.

    기록 형식:
        {"name": 함수이름, "args": (위치인자 튜플), "kwargs": {가려진 키워드인자}, "result": 반환값}

    SENSITIVE 에 든 이름의 키워드 인자는 값 대신 MASK("***") 를 기록합니다.
    예외가 나면 {"name":..., "error": "예외클래스이름"} 을 기록하고 예외를 다시 올립니다.
    functools.wraps 로 원본 메타데이터를 보존하세요.
    """
    raise NotImplementedError


class RateLimitError(Exception):
    """허용된 호출 횟수를 넘었을 때."""


def rate_limit(
    calls: int,
    per_seconds: float,
    *,
    clock: Callable[[], float] = time.monotonic,
) -> Callable:
    """per_seconds 안에 calls 번까지만 허용하고, 넘으면 RateLimitError 를 낸다.

    최근 호출 시각을 deque 에 담아 두고, 창(window) 밖으로 나간 것부터 버리세요.

    clock 을 인자로 받는 이유: 시간에 의존하는 코드를 그대로 두면 테스트가
    실제로 1초를 기다려야 합니다. 시계를 '주입 가능한 의존성'으로 만들면
    테스트에서 가짜 시계를 넣어 즉시 검증할 수 있습니다 (18파트의 주제입니다).
    """
    raise NotImplementedError


def timed(func: Callable) -> Callable:
    """동기 함수든 async 함수든 붙일 수 있는 실행 시간 측정 데코레이터.

    실행에 걸린 초를 TIMINGS[func.__name__] 에 넣습니다. 예외가 나도 기록해야 합니다.

    ⚠️ async 함수에 동기 wrapper 를 씌우면 코루틴 객체만 돌려주고 실행되지 않습니다.
       inspect.iscoroutinefunction(func) 으로 갈라 async wrapper 를 따로 만드세요.
       이건 조용히 실패하는 종류의 버그라 직접 겪어 볼 가치가 있습니다.
    """
    raise NotImplementedError
