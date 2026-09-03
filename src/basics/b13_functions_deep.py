"""B13 · 함수 더 깊이 — 인자·반환·스코프·재귀

B5에서 함수를 만드는 법을 배웠습니다. 여기서는 함수가 실제로 할 수 있는 일을 다 봅니다.

이번 파트에서 쓰는 도구:
    def f(a, *, b)        * 뒤의 인자는 **이름으로만** 넘길 수 있다
    def f(*args)          남는 위치 인자를 튜플로 모은다
    def f(**kwargs)       남는 키워드 인자를 딕셔너리로 모은다
    return a, b           여러 값을 튜플로 돌려준다
    lambda x: x + 1       이름 없는 짧은 함수
    global / nonlocal     바깥 변수에 **대입**할 때 필요
    함수 자체를 인자로 넘기고 반환할 수 있다 (일급 객체)
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

#: B13-7 에서 쓰는 모듈 전역 변수
COUNTER = 0


def make_url(host: str, *, port: int = 80, secure: bool = False) -> str:
    """URL 문자열을 만든다.

    make_url("a.com") == "http://a.com:80"
    make_url("a.com", port=443, secure=True) == "https://a.com:443"

    `*` 뒤의 인자는 **키워드 전용**입니다. make_url("a.com", 443) 은 TypeError 가 나야 합니다.

    왜 이렇게 쓰나: `make_url("a.com", 443, True)` 는 읽는 사람이 443과 True가 뭔지
    알 수 없습니다. 불리언 인자가 있으면 거의 항상 키워드 전용으로 만드세요.
    (시그니처는 이미 써 뒀습니다. 몸통만 채우세요)
    """
    raise NotImplementedError


def total(*numbers: int) -> int:
    """받은 수를 모두 더한다. 하나도 없으면 0.

    total(1, 2, 3) == 6
    total() == 0

    *numbers 는 위치 인자를 **튜플로** 모읍니다. 개수를 미리 정하지 않아도 됩니다.
    """
    raise NotImplementedError


def build_tag(name: str, **attrs: str) -> str:
    """HTML 여는 태그를 만든다. 속성은 넘긴 순서대로.

    build_tag("a") == "<a>"
    build_tag("a", href="x", id="y") == '<a href="x" id="y">'

    **attrs 는 키워드 인자를 **딕셔너리로** 모읍니다. 순서는 넘긴 순서 그대로 유지됩니다.
    """
    raise NotImplementedError


def min_max(numbers: list[int]) -> tuple[int, int]:
    """(최솟값, 최댓값) 을 한 번에 돌려준다. 빈 리스트면 ValueError.

    min_max([3, 1, 2]) == (1, 3)
    lo, hi = min_max([3, 1, 2])        # 이렇게 나눠 받는 걸 '언패킹'이라 합니다

    파이썬은 `return a, b` 로 여러 값을 돌려줍니다. 사실은 튜플 하나를 돌려주는 것이고,
    받는 쪽에서 나눠 담는 것입니다.
    """
    raise NotImplementedError


def apply_twice(func: Callable[[Any], Any], value: Any) -> Any:
    """func 를 value 에 두 번 적용한다.

    apply_twice(lambda x: x + 1, 1) == 3
    apply_twice(str.upper, "a") == "A"

    파이썬에서 함수는 **값**입니다. 변수에 담고, 인자로 넘기고, 돌려줄 수 있습니다.
    sorted(key=...) 나 데코레이터가 전부 이 성질 위에 서 있습니다.
    """
    raise NotImplementedError


def make_multiplier(n: int) -> Callable[[int], int]:
    """n 을 곱하는 함수를 **만들어서 돌려준다**.

    double = make_multiplier(2)
    double(5) == 10
    triple = make_multiplier(3)
    triple(5) == 15                    # double 과 서로 영향이 없어야 합니다

    안쪽 함수가 바깥 함수의 n 을 기억합니다. 이걸 '클로저'라고 합니다.
    """
    raise NotImplementedError


def make_accumulator() -> Callable[[int], int]:
    """더한 값을 누적해 돌려주는 함수를 만든다.

    acc = make_accumulator()
    acc(10) == 10
    acc(5) == 15                       # 이전 값을 기억한다

    ⚠️ 안쪽 함수에서 바깥 변수에 **대입**하려면 `nonlocal` 이 필요합니다.
       그냥 `total = total + n` 이라고 쓰면 파이썬은 새 지역 변수를 만들고
       UnboundLocalError 를 냅니다. 읽기만 할 땐 필요 없습니다(make_multiplier 처럼).
    """
    raise NotImplementedError


def bump() -> int:
    """모듈 전역 COUNTER 를 1 올리고 그 값을 돌려준다.

    reset_counter(); bump() == 1; bump() == 2

    ⚠️ 전역 변수에 **대입**하려면 함수 안에서 `global COUNTER` 를 선언해야 합니다.

    그리고 이 문제의 진짜 교훈: **전역 변수는 되도록 쓰지 마세요.**
    누가 언제 바꿨는지 추적할 수 없고, 테스트마다 초기화해 줘야 합니다
    (그래서 아래 reset_counter 가 필요한 겁니다). make_accumulator 쪽이 낫습니다.
    """
    raise NotImplementedError


def reset_counter() -> None:
    """COUNTER 를 0으로. (이미 돼 있습니다 — bump 를 만들 때 참고하세요)"""
    global COUNTER
    COUNTER = 0


def factorial(n: int) -> int:
    """n! 을 재귀로 계산한다. 0! 은 1.

    factorial(5) == 120
    factorial(0) == 1

    재귀에는 반드시 두 부분이 있습니다:
        멈추는 조건(기저)   n 이 0이면 1
        자기를 부르는 부분   n * factorial(n - 1)
    기저를 빠뜨리면 RecursionError 가 납니다.
    """
    raise NotImplementedError


def sum_nested(nested: list[Any]) -> int:
    """중첩된 리스트 안의 숫자를 전부 더한다.

    sum_nested([1, [2, [3, 4]], 5]) == 15
    sum_nested([]) == 0

    원소가 리스트면 자기 자신을 부르고, 숫자면 그냥 더하세요.
    깊이를 모르는 구조에는 반복문보다 재귀가 자연스럽습니다.
    """
    raise NotImplementedError


def append_safe(item: Any, target: list[Any] | None = None) -> list[Any]:
    """target 에 item 을 붙여 돌려준다. target 을 안 주면 새 리스트를 만든다.

    append_safe(1) == [1]
    append_safe(2) == [2]              # 앞 호출과 **독립**이어야 합니다
    append_safe(3, [0]) == [0, 3]

    ⚠️ `def append_safe(item, target=[])` 라고 쓰면 안 됩니다.
       기본값은 함수가 **정의될 때 한 번** 만들어져 함수 객체에 붙습니다.
       그래서 호출할 때마다 같은 리스트에 쌓입니다: [1], [1, 2], [1, 2, 3]...
       가변 기본값은 항상 None 으로 두고 함수 안에서 만드세요.
    """
    raise NotImplementedError
