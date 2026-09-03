"""B1 모범답안."""

from __future__ import annotations


def introduce(name: str, age: int, height: float) -> str:
    return f"{name}님은 {age}살, 키는 {height}cm입니다"


def add_to_price(price: int, extra: int) -> int:
    price = price + extra
    return price


def swap(a: object, b: object) -> tuple[object, object]:
    a, b = b, a
    return a, b


def total_seconds(days: int) -> int:
    seconds_per_day = 86_400
    return days * seconds_per_day
