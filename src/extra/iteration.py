"""확장 08 — 이터레이션   (docs/17_core_08.md DRILL 08)"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable, Iterator
from typing import Any


def fib() -> Iterator[int]:
    """0, 1, 1, 2, 3, 5, 8 ... 을 끝없이 내는 제너레이터.

    끝이 없어야 합니다. islice 로 앞부분만, takewhile 로 조건까지만 뽑아 쓰게 됩니다.
    리스트를 만들어 반환하면 무한 수열이 될 수 없습니다.
    """
    raise NotImplementedError


def unique_everseen(iterable: Iterable, key: Callable[[Any], Hashable] | None = None) -> Iterator:
    """중복을 건너뛰며 **게으르게** 하나씩 내보낸다. 순서는 처음 나온 순.

    list(unique_everseen("AAABBC")) == ["A", "B", "C"]
    key 를 주면 그 결과로 중복을 판정합니다.
    무한 이터러블에도 붙일 수 있어야 하니 전부 모았다가 반환하면 안 됩니다.
    """
    raise NotImplementedError


def parse_jsonl(lines: Iterable[str]) -> Iterator[dict]:
    """JSON Lines 를 dict 로 하나씩 내보낸다. 빈 줄(공백만 있는 줄)은 건너뛴다.

    깨진 줄이 있으면 ValueError 를 그대로 올려 보내세요(여기서 삼키지 않습니다).
    """
    raise NotImplementedError


def jsonl_batches(
    lines: Iterable[str],
    pred: Callable[[dict], bool],
    size: int,
) -> Iterator[list[dict]]:
    """JSONL 을 읽어 조건에 맞는 레코드만 size개씩 배치로 넘긴다.

    파일 전체를 리스트로 만들지 말고, parse → filter → batch 세 단계를
    전부 제너레이터로 이어 붙이세요. 그래야 100GB 파일도 같은 코드로 처리됩니다.
    마지막 배치는 size 보다 작을 수 있습니다. 조건에 맞는 게 없으면 아무것도 내지 않습니다.
    """
    raise NotImplementedError
