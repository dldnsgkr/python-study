"""코어 06~09 — 제어 흐름 · 함수 · 이터레이션 · 데코레이터

docs/15_core_06.md ~ docs/18_core_09.md
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Any


# ── 06 제어 흐름 ───────────────────────────────────────────
def first_match(xs: Iterable, pred: Callable[[Any], bool], default: Any = None) -> Any:
    """조건을 만족하는 첫 원소. 없으면 default.

    ⚠️ 무한 이터러블에서도 즉시 반환해야 합니다.
       [x for x in xs if pred(x)][0] 처럼 전부 만들어 놓고 고르면 영원히 안 끝납니다.
    """
    raise NotImplementedError


def transpose(matrix: list[list]) -> list[list]:
    """행과 열을 뒤집는다. [[1,2,3],[4,5,6]] -> [[1,4],[2,5],[3,6]]

    컴프리헨션과 zip(*matrix) 두 방법으로 각각 짜 보고 차이를 설명해 보세요.
    """
    raise NotImplementedError


# ── 07 함수 ────────────────────────────────────────────────
def make_counter(start: int = 0) -> Callable[[], int]:
    """호출할 때마다 1씩 증가한 값을 반환하는 함수를 만든다(클로저).

    c = make_counter(); [c(), c(), c()] == [1, 2, 3]
    make_counter(10) 의 첫 호출은 11 입니다.
    카운터끼리는 서로 영향을 주지 않아야 합니다.
    """
    raise NotImplementedError


def bind_args(func: Callable, *args: Any, **kwargs: Any) -> dict:
    """호출 인자를 기본값까지 반영한 {이름: 값} dict로 정규화한다.

    def f(a, b=2, *, c=3): ...
    bind_args(f, 1) == {"a": 1, "b": 2, "c": 3}
    힌트: inspect.signature(...).bind(...) 와 apply_defaults()
    """
    raise NotImplementedError


# ── 08 이터레이션 ──────────────────────────────────────────
def window(iterable: Iterable, n: int) -> Iterator[tuple]:
    """길이 n의 슬라이딩 윈도우. 원소가 n개 미만이면 아무것도 내지 않는다.

    list(window([1,2,3,4], 2)) == [(1,2), (2,3), (3,4)]
    함정: deque 버퍼를 그대로 yield 하면 소비자가 보는 값이 다음 루프에서 바뀝니다.
          매번 tuple(...) 로 복사해 내보내세요.
    무한 이터러블에서도 동작해야 합니다.
    """
    raise NotImplementedError


def batches(iterable: Iterable, size: int) -> Iterator[list]:
    """size개씩 묶어 낸다. 마지막 배치는 더 작을 수 있다.

    list(batches(range(7), 3)) == [[0,1,2], [3,4,5], [6]]
    """
    raise NotImplementedError


# ── 09 데코레이터 ──────────────────────────────────────────
def retry(times: int = 3, exceptions: tuple[type[BaseException], ...] = (Exception,)) -> Callable:
    """실패하면 다시 시도하는 데코레이터.

    times 는 **총 시도 횟수**입니다(재시도 횟수가 아닙니다).
      times=3 이면 최대 3번 호출하고, 3번째도 실패하면 그 예외를 그대로 올립니다.
    exceptions 에 없는 예외는 재시도하지 말고 즉시 통과시키세요.
    functools.wraps 로 __name__ · __doc__ 을 보존해야 합니다.
    """
    raise NotImplementedError
