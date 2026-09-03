"""확장 08 모범답안."""

from __future__ import annotations

import json
from collections.abc import Callable, Hashable, Iterable, Iterator
from itertools import islice
from typing import Any


def fib() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def unique_everseen(iterable: Iterable, key: Callable[[Any], Hashable] | None = None) -> Iterator:
    seen: set = set()
    for item in iterable:
        marker = item if key is None else key(item)
        if marker not in seen:
            seen.add(marker)
            yield item


def parse_jsonl(lines: Iterable[str]) -> Iterator[dict]:
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        yield json.loads(stripped)


def jsonl_batches(
    lines: Iterable[str],
    pred: Callable[[dict], bool],
    size: int,
) -> Iterator[list[dict]]:
    matched = (record for record in parse_jsonl(lines) if pred(record))
    while chunk := list(islice(matched, size)):
        yield chunk
