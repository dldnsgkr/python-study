"""B9 모범답안."""

from __future__ import annotations

from typing import Any


def numbered(items: list[str]) -> list[str]:
    return [f"{i}. {item}" for i, item in enumerate(items, start=1)]


def pair_up(names: list[str], scores: list[int]) -> dict[str, int]:
    return dict(zip(names, scores, strict=False))


def invert(mapping: dict[str, int]) -> dict[int, str]:
    return {value: key for key, value in mapping.items()}


def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_two(scores: list[int]) -> list[int]:
    return sorted(scores, reverse=True)[:2]


def rank_names(students: list[dict[str, Any]]) -> list[str]:
    ordered = sorted(students, key=lambda s: s["score"], reverse=True)
    return [s["name"] for s in ordered]


def remove_all(xs: list[Any], value: Any) -> list[Any]:
    return [x for x in xs if x != value]


def flatten_once(nested: list[list[Any]]) -> list[Any]:
    out: list[Any] = []
    for inner in nested:
        out.extend(inner)
    return out


def has_duplicate(xs: list[Any]) -> bool:
    return len(set(xs)) != len(xs)
