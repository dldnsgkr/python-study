"""코어 10~13 모범답안."""

from __future__ import annotations

import json
from enum import StrEnum
from functools import total_ordering
from typing import Any


class Temperature:
    def __init__(self, celsius: float = 0.0) -> None:
        self.celsius = celsius

    @property
    def fahrenheit(self) -> float:
        return self.celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5 / 9


@total_ordering
class Money:
    __slots__ = ("amount", "currency")

    def __init__(self, amount: int, currency: str = "KRW") -> None:
        self.amount = amount
        self.currency = currency

    def _check(self, other: Any) -> None:
        if not isinstance(other, Money) or other.currency != self.currency:
            raise TypeError("통화가 다릅니다")

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Money)
            and self.currency == other.currency
            and self.amount == other.amount
        )

    def __lt__(self, other: Any) -> bool:
        self._check(other)
        return self.amount < other.amount

    def __add__(self, other: Any) -> Money:
        self._check(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Any) -> Money:
        self._check(other)
        return Money(self.amount - other.amount, self.currency)

    def __radd__(self, other: Any) -> Money:
        return self if other == 0 else self.__add__(other)   # sum() 은 0에서 시작한다

    def __hash__(self) -> int:
        return hash((self.amount, self.currency))

    def __repr__(self) -> str:
        return f"Money({self.amount}, {self.currency!r})"


class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"


TRANSITIONS: dict[Status, set[Status]] = {
    Status.PENDING: {Status.PAID, Status.CANCELED},
    Status.PAID: {Status.CANCELED},
    Status.CANCELED: set(),
}


def transition(current: Status, nxt: Status) -> Status:
    if nxt not in TRANSITIONS[current]:
        raise ValueError(f"{current} → {nxt} 전이 불가")
    return nxt


class ConfigError(Exception):
    """설정을 읽지 못했을 때 쓰는 도메인 예외."""


def load_config(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise ConfigError(f"설정 파일이 없습니다: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"설정 파일이 올바른 JSON이 아닙니다: {path}") from exc
