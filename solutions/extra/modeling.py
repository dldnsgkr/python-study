"""확장 12 모범답안."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

REQUIRED = ("sku", "qty", "unit_price")


@dataclass(frozen=True, kw_only=True)
class OrderLine:
    sku: str
    qty: int
    unit_price: int

    def __post_init__(self) -> None:
        if self.qty <= 0:
            raise ValueError("수량은 1 이상이어야 합니다")
        if self.unit_price < 0:
            raise ValueError("단가는 음수일 수 없습니다")

    @property
    def total(self) -> int:
        return self.qty * self.unit_price


class OrderPayload(TypedDict):
    sku: str
    qty: int
    unit_price: int


def from_payload(payload: OrderPayload) -> OrderLine:
    missing = [key for key in REQUIRED if key not in payload]
    if missing:
        raise ValueError(f"필수 키 누락: {', '.join(missing)}")
    return OrderLine(
        sku=payload["sku"],
        qty=payload["qty"],
        unit_price=payload["unit_price"],
    )
