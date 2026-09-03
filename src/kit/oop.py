"""코어 10~13 — 클래스 · 특수 메서드 · 데이터 모델링 · 예외

docs/19_core_10.md ~ docs/22_core_13.md
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any


# ── 10 클래스 ──────────────────────────────────────────────
class Temperature:
    """celsius를 저장하고 fahrenheit를 읽기/쓰기 가능한 property로 제공한다.

    t = Temperature(100); t.fahrenheit == 212
    t.fahrenheit = 32   ->  t.celsius == 0

    fahrenheit 를 __init__ 에서 계산해 필드로 저장하면 안 됩니다.
    celsius 를 바꿨을 때 따라 바뀌지 않으니까요 — property 로 그때그때 계산하세요.
    """

    def __init__(self, celsius: float = 0.0) -> None:
        raise NotImplementedError


# ── 11 특수 메서드 ─────────────────────────────────────────
class Money:
    """금액과 통화를 담는 값 객체.

    - 같은 통화끼리만 +, -, 비교가 된다. 통화가 다르면 TypeError.
    - sum([Money(100), Money(200)]) 이 동작해야 한다 (__radd__ 가 필요합니다.
      sum 은 0 에서 시작하므로 0 + Money 를 처리해야 하니까요).
    - 같은 금액·통화면 == 이고 set 에 넣었을 때 하나로 합쳐진다 (__hash__).
    - repr(Money(100)) 에 금액이 보여야 한다.

    힌트: functools.total_ordering 을 쓰면 __eq__ 와 __lt__ 만으로 충분합니다.
    """

    def __init__(self, amount: int, currency: str = "KRW") -> None:
        raise NotImplementedError


# ── 12 데이터 모델링 ───────────────────────────────────────
class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"


def transition(current: Status, nxt: Status) -> Status:
    """허용된 전이만 통과시키고, 아니면 ValueError를 낸다.

    허용: PENDING -> PAID, PENDING -> CANCELED, PAID -> CANCELED
    CANCELED 에서는 어디로도 갈 수 없습니다.
    if 문을 늘어놓지 말고 dict 기반 전이표로 만드세요.
    """
    raise NotImplementedError


# ── 13 예외 ────────────────────────────────────────────────
class ConfigError(Exception):
    """설정을 읽지 못했을 때 쓰는 도메인 예외."""


def load_config(path: str) -> dict:
    """JSON 설정 파일을 읽어 dict 로 돌려준다.

    파일이 없거나 JSON 이 깨졌으면 ConfigError 로 바꿔 던지되,
    원인 예외를 __cause__ 로 보존하세요 (`raise ConfigError(...) from exc`).

    호출한 쪽은 FileNotFoundError 를 알 필요가 없지만,
    디버깅할 사람은 진짜 원인을 볼 수 있어야 합니다. 그 둘을 동시에 만족시키는 게 from 입니다.
    """
    raise NotImplementedError
