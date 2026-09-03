"""확장 05 모범답안."""

from __future__ import annotations

import copy
from typing import Any


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity 는 1 이상이어야 합니다")
        self.capacity = capacity
        self._data: dict = {}

    def get(self, key: Any, default: Any = None) -> Any:
        if key not in self._data:
            return default
        value = self._data.pop(key)
        self._data[key] = value       # 지웠다 다시 넣으면 삽입 순서상 맨 뒤로 간다
        return value

    def put(self, key: Any, value: Any) -> None:
        if key in self._data:
            del self._data[key]
        elif len(self._data) >= self.capacity:
            oldest = next(iter(self._data))
            del self._data[oldest]
        self._data[key] = value

    def keys(self) -> list:
        return list(self._data)

    def __len__(self) -> int:
        return len(self._data)


def merge_deep(base: dict, override: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(result.get(key), dict) and isinstance(value, dict):
            result[key] = merge_deep(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result
