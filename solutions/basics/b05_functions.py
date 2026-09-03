"""B5 모범답안."""

from __future__ import annotations


def multiply(a: int, b: int) -> int:
    return a * b


def welcome(name: str) -> str:
    return f"환영합니다, {name}님"


def to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32


def average(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("빈 리스트의 평균은 없습니다")
    return sum(numbers) / len(numbers)


def apply_discount(price: int, rate: float = 0.1) -> int:
    return int(price * (1 - rate))
