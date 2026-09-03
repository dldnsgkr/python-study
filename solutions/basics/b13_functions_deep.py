"""B13 모범답안."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

COUNTER = 0


def make_url(host: str, *, port: int = 80, secure: bool = False) -> str:
    scheme = "https" if secure else "http"
    return f"{scheme}://{host}:{port}"


def total(*numbers: int) -> int:
    return sum(numbers)


def build_tag(name: str, **attrs: str) -> str:
    if not attrs:
        return f"<{name}>"
    parts = " ".join(f'{key}="{value}"' for key, value in attrs.items())
    return f"<{name} {parts}>"


def min_max(numbers: list[int]) -> tuple[int, int]:
    if not numbers:
        raise ValueError("빈 리스트에는 최솟값도 최댓값도 없습니다")
    return min(numbers), max(numbers)


def apply_twice(func: Callable[[Any], Any], value: Any) -> Any:
    return func(func(value))


def make_multiplier(n: int) -> Callable[[int], int]:
    def multiply(x: int) -> int:
        return x * n            # 읽기만 하므로 nonlocal 이 필요 없다
    return multiply


def make_accumulator() -> Callable[[int], int]:
    running = 0

    def add(n: int) -> int:
        nonlocal running        # 대입하려면 nonlocal 이 필요하다
        running += n
        return running

    return add


def bump() -> int:
    global COUNTER
    COUNTER += 1
    return COUNTER


def reset_counter() -> None:
    global COUNTER
    COUNTER = 0


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError(f"음수의 팩토리얼은 없습니다: {n}")
    if n == 0:
        return 1                # 기저 — 이게 없으면 RecursionError
    return n * factorial(n - 1)


def sum_nested(nested: list[Any]) -> int:
    total_sum = 0
    for item in nested:
        if isinstance(item, list):
            total_sum += sum_nested(item)
        else:
            total_sum += item
    return total_sum


def append_safe(item: Any, target: list[Any] | None = None) -> list[Any]:
    target = [] if target is None else target
    target.append(item)
    return target
