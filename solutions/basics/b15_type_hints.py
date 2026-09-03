"""B15 모범답안."""

from __future__ import annotations

from typing import Any


def repeat(text: str, times: int = 2) -> str:
    return text * times


def first_or_none(xs: list[int]) -> int | None:
    return xs[0] if xs else None


def count_lengths(words: list[str]) -> dict[str, int]:
    return {word: len(word) for word in words}


def parse_pair(text: str) -> tuple[str, int]:
    name, sep, raw = text.partition(":")
    if not sep:
        raise ValueError(f"'이름:숫자' 형식이 아닙니다: {text!r}")
    return name, int(raw)


def to_int(value: str | float | bool) -> int:
    return int(value)


def describe_all(items: list[Any]) -> list[str]:
    return [f"{type(item).__name__}:{item}" for item in items]


def safe_len(value: str | list[Any] | dict[str, Any] | None) -> int:
    if value is None:
        return 0
    return len(value)
