"""코어 01~05 모범답안."""

from __future__ import annotations

import copy
from collections.abc import Callable, Hashable, Iterable
from decimal import ROUND_HALF_UP, Decimal
from typing import Any


def with_key(d: dict, path: list[str], value: Any) -> dict:
    result = copy.deepcopy(d)
    cursor = result
    for key in path[:-1]:
        cursor = cursor.setdefault(key, {})
    cursor[path[-1]] = value
    return result


def total_with_vat(unit_price: str, qty: int) -> Decimal:
    subtotal = Decimal(unit_price) * qty
    return (subtotal * Decimal("1.1")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def split_once(s: str, sep: str = "=") -> tuple[str, str]:
    head, _, tail = s.partition(sep)
    return head, tail


def rotate(xs: list, k: int) -> list:
    if not xs:
        return []
    k %= len(xs)
    return xs[-k:] + xs[:-k] if k else xs[:]


def flatten(xs: Iterable) -> list:
    out: list = []
    for item in xs:
        if isinstance(item, list | tuple):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out


def group_by(records: Iterable[Any], key: Callable[[Any], Hashable]) -> dict:
    groups: dict = {}
    for record in records:
        groups.setdefault(key(record), []).append(record)
    return groups


def diff(old: dict, new: dict) -> dict:
    old_keys, new_keys = set(old), set(new)
    common = old_keys & new_keys
    return {
        "added": {k: new[k] for k in new_keys - old_keys},
        "removed": {k: old[k] for k in old_keys - new_keys},
        "changed": {k: (old[k], new[k]) for k in common if old[k] != new[k]},
    }
