"""확장 19 모범답안."""

from __future__ import annotations

import heapq
from collections import Counter
from collections.abc import Callable, Hashable, Iterable
from typing import Any


def intersect(a: Iterable[Hashable], b: Iterable[Hashable]) -> list:
    lookup = set(b)                 # 리스트 스캔 O(m) 을 해시 조회 O(1) 로 바꾼다
    seen: set = set()
    out: list = []
    for item in a:
        if item in lookup and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def top_n(iterable: Iterable, n: int, key: Callable[[Any], Any] | None = None) -> list:
    if n <= 0:
        return []
    return heapq.nlargest(n, iterable, key=key)


def stream_word_count(path: str) -> Counter:
    counter: Counter[str] = Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:                       # 파일 전체가 아니라 한 줄씩
            counter.update(word.lower() for word in line.split())
    return counter
