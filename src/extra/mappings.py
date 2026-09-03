"""확장 05 — 매핑과 집합   (docs/14_core_05.md DRILL 05)"""

from __future__ import annotations

from typing import Any


class LRUCache:
    """용량이 정해진 LRU 캐시. **dict의 삽입 순서 보장만** 이용해 구현하세요.

    OrderedDict.move_to_end 를 쓰지 마세요. 평범한 dict 로도
    "지우고 다시 넣으면 맨 뒤로 간다"는 성질을 이용해 같은 걸 만들 수 있습니다.

    cache = LRUCache(2)
    cache.put("a", 1); cache.put("b", 2)
    cache.get("a")            # a 를 최근 사용으로 끌어올린다
    cache.put("c", 3)         # 가장 오래된 b 가 밀려난다
    cache.keys() == ["a", "c"]     # 오래된 것 → 최근 것 순서

    - get(key, default=None): 없으면 default, 있으면 최근 사용으로 갱신
    - put(key, value): 이미 있으면 값 갱신 + 최근 사용으로
    - len(cache): 현재 항목 수
    """

    def __init__(self, capacity: int) -> None:
        raise NotImplementedError

    def get(self, key: Any, default: Any = None) -> Any:
        raise NotImplementedError

    def put(self, key: Any, value: Any) -> None:
        raise NotImplementedError

    def keys(self) -> list:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


def merge_deep(base: dict, override: dict) -> dict:
    """중첩 dict를 재귀적으로 병합한 새 dict를 돌려준다. 원본 둘 다 건드리지 않는다.

    merge_deep({"a": {"x": 1, "y": 2}}, {"a": {"y": 9}}) == {"a": {"x": 1, "y": 9}}

    dict 가 아닌 값끼리 만나면 override 쪽이 이깁니다.
    설정 파일(기본값 + 사용자 설정)을 합칠 때 실제로 매번 쓰는 함수입니다.
    """
    raise NotImplementedError
