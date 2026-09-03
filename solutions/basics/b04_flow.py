"""B4 모범답안."""

from __future__ import annotations


def sign(n: int) -> str:
    if n > 0:
        return "양수"
    elif n < 0:
        return "음수"
    else:
        return "0"


def times_table(n: int) -> list[str]:
    return [f"{n} x {i} = {n * i}" for i in range(1, 10)]


def sum_to(n: int) -> int:
    if n <= 0:
        return 0
    return sum(range(1, n + 1))


def bigger_than(numbers: list[int], threshold: int) -> list[int]:
    return [n for n in numbers if n > threshold]


def grade(score: int) -> str:
    if not 0 <= score <= 100:
        raise ValueError(f"점수는 0~100 이어야 합니다: {score}")
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "F"
