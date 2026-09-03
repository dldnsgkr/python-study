"""B2 모범답안."""

from __future__ import annotations


def describe_type(value: object) -> str:
    return type(value).__name__


def greet(name: str, age: int) -> str:
    return f"{name}님은 {age}살입니다"


def divide_report(a: int, b: int) -> tuple[float, int, int]:
    return a / b, a // b, a % b


def is_even(n: int) -> bool:
    return n % 2 == 0


def sum_of_inputs(a: str, b: str) -> int:
    return int(a) + int(b)
