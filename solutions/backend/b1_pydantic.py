"""B1 모범답안."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

ORDER_LIMIT = Decimal(10_000_000)


class SignUp(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def validate_password(self) -> SignUp:
        if len(self.password) < 8:
            raise ValueError("비밀번호는 8자 이상이어야 합니다")
        if not (re.search(r"[A-Za-z]", self.password) and re.search(r"\d", self.password)):
            raise ValueError("영문과 숫자를 모두 포함해야 합니다")
        if self.password != self.password_confirm:
            raise ValueError("비밀번호가 일치하지 않습니다")
        return self


def describe_errors(exc: ValidationError) -> list[dict[str, str]]:
    summary: list[dict[str, str]] = []
    for error in exc.errors():
        loc = ".".join(str(part) for part in error["loc"])
        summary.append({
            "field": loc or "__root__",
            "type": error["type"],
            "msg": error["msg"],
        })
    return summary


class OrderLineIn(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    qty: int = Field(gt=0, le=999)
    unit_price: Decimal = Field(ge=0, decimal_places=2)


class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    customer_id: int
    lines: list[OrderLineIn] = Field(min_length=1)
    memo: str | None = None

    @field_validator("memo")
    @classmethod
    def no_html(cls, v: str | None) -> str | None:
        if v and "<" in v:
            raise ValueError("HTML 태그는 사용할 수 없습니다")
        return v

    @model_validator(mode="after")
    def check_total(self) -> OrderCreate:
        total = sum((line.qty * line.unit_price for line in self.lines), Decimal(0))
        if total > ORDER_LIMIT:
            raise ValueError("단일 주문 한도를 초과했습니다")
        return self


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")

    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    debug: bool = False
    max_workers: int = 4


@dataclass(frozen=True)
class DomainLine:
    sku: str
    qty: int
    unit_price: Decimal


@dataclass(frozen=True)
class DomainOrder:
    customer_id: int
    lines: tuple[DomainLine, ...]
    memo: str | None = None

    @property
    def total(self) -> Decimal:
        return sum((line.qty * line.unit_price for line in self.lines), Decimal(0))


def to_domain(payload: OrderCreate) -> DomainOrder:
    return DomainOrder(
        customer_id=payload.customer_id,
        lines=tuple(
            DomainLine(sku=line.sku, qty=line.qty, unit_price=line.unit_price)
            for line in payload.lines
        ),
        memo=payload.memo,
    )
