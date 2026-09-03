"""확장 03 모범답안."""

from __future__ import annotations

import unicodedata


def format_row(name: str, amount: float) -> str:
    return f"{name:<12}{amount:>10,.2f}"


def parse_csv_line(line: str) -> list[str | None]:
    return [field.strip() or None for field in line.split(",")]


def display_width(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in s)


def pad_display(s: str, width: int) -> str:
    padding = width - display_width(s)
    return s + " " * padding if padding > 0 else s
