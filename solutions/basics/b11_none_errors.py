"""B11 모범답안."""

from __future__ import annotations

from typing import Any


def find_user(users: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    for user in users:
        if user.get("name") == name:
            return user
    return None


def display_name(user: dict[str, Any] | None) -> str:
    if user is None:
        return "손님"
    return str(user["name"])


def safe_int(text: str, default: int = 0) -> int:
    try:
        return int(text)
    except ValueError:
        return default


def safe_divide(a: float, b: float) -> float | None:
    try:
        return a / b
    except ZeroDivisionError:
        return None


def require_positive(n: int) -> int:
    if n <= 0:
        raise ValueError(f"0보다 커야 합니다: {n}")
    return n


def parse_scores(raw: list[str]) -> list[int]:
    scores: list[int] = []
    for item in raw:
        try:
            scores.append(int(item))
        except ValueError:
            continue
    return scores


def divide_with_log(a: float, b: float, log: list[str]) -> float | None:
    try:
        log.append("시도")
        result = a / b
    except ZeroDivisionError:
        log.append("실패")
        return None
    else:
        log.append("성공")     # 예외가 안 났을 때만
        return result
    finally:
        log.append("정리")     # 났든 안 났든 반드시
