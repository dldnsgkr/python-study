"""B1 · 변수 — 값에 이름 붙이기   (docs/02_basics_B1.md)

`=` 는 "같다"가 아니라 "오른쪽 값을 왼쪽 이름에 넣어라"입니다.
아래 함수들의 `raise NotImplementedError` 를 지우고 직접 구현하세요.

💡 `name: str` 이나 `-> str` 이 뭔지 궁금하다면 — **타입 힌트**입니다.
   "이 자리에는 문자열이 온다", "문자열을 돌려준다"는 메모이고,
   런타임에는 아무 일도 하지 않습니다. 지금은 무시해도 됩니다. B15에서 제대로 배웁니다.
"""

from __future__ import annotations


def introduce(name: str, age: int, height: float) -> str:
    """자기소개 한 줄을 만들어 돌려준다.

    introduce("김파이", 25, 172.5) == "김파이님은 25살, 키는 172.5cm입니다"
    """
    raise NotImplementedError


def add_to_price(price: int, extra: int) -> int:
    """price 에 extra 를 더한 값을 돌려준다.

    `price = price + extra` 가 왜 말이 되는지 생각해 보세요.
    오른쪽을 먼저 계산한 뒤 그 결과를 이름에 다시 묶습니다.
    """
    raise NotImplementedError


def swap(a: object, b: object) -> tuple[object, object]:
    """두 값을 바꿔 (b, a) 형태로 돌려준다.

    임시 변수를 쓰는 방법과 `a, b = b, a` 두 가지를 모두 시도해 보세요.
    """
    raise NotImplementedError


def total_seconds(days: int) -> int:
    """며칠이 몇 초인지 계산한다.

    86400 을 그냥 쓰지 말고 `seconds_per_day` 같은 이름을 먼저 만들어 보세요.
    좋은 이름이 좋은 코드입니다.
    """
    raise NotImplementedError
