"""확장 19 — 성능   (docs/28_core_19.md DRILL 19)"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Hashable, Iterable
from typing import Any


def intersect(a: Iterable[Hashable], b: Iterable[Hashable]) -> list:
    """두 컬렉션의 교집합을 a의 순서를 유지한 리스트로 돌려준다. 중복 없음.

    intersect([3, 1, 2, 1], [1, 3]) == [3, 1]

    ⚠️ `if x in b` 로 리스트를 매번 스캔하면 O(n*m) 입니다.
       10만 건 두 개면 테스트 시간 제한에 걸립니다. b 를 먼저 set 으로 바꾸세요.
    """
    raise NotImplementedError


def top_n(iterable: Iterable, n: int, key: Callable[[Any], Any] | None = None) -> list:
    """가장 큰 n개를 내림차순으로 돌려준다.

    전부 정렬하면 O(N log N) 이지만, n 이 작으면 heapq 로 O(N log n) 입니다.
    100만 건에서 상위 10개를 뽑을 때 실제로 차이가 납니다.
    n 이 0 이하면 빈 리스트, 원소 수보다 크면 있는 만큼만.
    """
    raise NotImplementedError


def stream_word_count(path: str) -> Counter:
    """파일의 단어 빈도를 센다. **파일 전체를 메모리에 올리지 않고** 한 줄씩.

    f.read().split() 은 파일 크기만큼 메모리를 씁니다.
    for line in f: 는 한 줄씩만 씁니다 — 파일이 100GB 여도 같은 코드가 돕니다.
    단어는 공백 기준으로 나누고 소문자로 통일하세요.
    """
    raise NotImplementedError
