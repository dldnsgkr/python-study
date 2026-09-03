"""B10 모범답안."""

from __future__ import annotations


def countdown(n: int) -> list[int]:
    out: list[int] = []
    while n > 0:
        out.append(n)
        n -= 1              # 이 줄을 빠뜨리면 영원히 돈다
    return out


def first_negative(numbers: list[int]) -> int | None:
    for number in numbers:
        if number < 0:
            return number   # 찾는 순간 멈춘다
    return None


def skip_comments(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        out.append(stripped)
    return out


def every_nth(start: int, end: int, step: int) -> list[int]:
    return list(range(start, end, step))


def all_pairs(xs: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            pairs.append((xs[i], xs[j]))
    return pairs


def squares(numbers: list[int]) -> list[int]:
    return [x * x for x in numbers]


def long_words(words: list[str], min_length: int) -> list[str]:
    return [w for w in words if len(w) >= min_length]


def word_lengths(words: list[str]) -> dict[str, int]:
    return {w: len(w) for w in words}
