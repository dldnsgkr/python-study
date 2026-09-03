"""B3 모범답안."""

from __future__ import annotations


def add_food(foods: list[str], new_food: str) -> tuple[str, str]:
    updated = [*foods, new_food]
    return updated[0], updated[-1]


def profile_lines(profile: dict[str, object]) -> list[str]:
    return [f"{key}: {value}" for key, value in profile.items()]


def unique_sorted(numbers: list[int]) -> list[int]:
    return sorted(set(numbers))


def add_hobby(profile: dict[str, object], hobby: str) -> dict[str, object]:
    return {**profile, "취미": hobby}


def has_key(profile: dict[str, object], key: str) -> bool:
    return key in profile
