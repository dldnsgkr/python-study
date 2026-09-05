"""B5 · 함수 — 나만의 명령 만들기   (docs/06_basics_B5.md)"""

from __future__ import annotations


def multiply(a: int, b: int) -> int:
    """두 수의 곱을 돌려준다."""
    return a * b


def welcome(name: str) -> str:
    """"환영합니다, OOO님" 을 **돌려준다**.

    print 하지 마세요. print 는 화면에 보여줄 뿐 값을 돌려주지 않습니다.
    돌려주는 함수라야 결과를 변수에 담고 다시 쓸 수 있습니다.
    """
    return f"환영합니다, {name}님"


def to_fahrenheit(celsius: float) -> float:
    """섭씨를 화씨로. 화씨 = 섭씨 × 9/5 + 32"""
    return celsius * 9/5 + 32


def average(numbers: list[float]) -> float:
    """평균을 돌려준다. sum() 과 len() 을 쓰세요.

    ⚠️ 빈 리스트가 오면 ValueError("빈 리스트의 평균은 없습니다") 를 내세요.
       그냥 두면 ZeroDivisionError 가 나는데, 그건 "왜 터졌는지" 를 알려주지 않습니다.
    """
    if(len(numbers) == 0):
        raise ValueError("빈 리스트의 평균은 없습니다")
    else:
        return sum(numbers) / len(numbers)


def apply_discount(price: int, rate: float = 0.1) -> int:
    """할인가를 정수로(내림) 돌려준다. rate 를 안 주면 10% 할인.

    기본값이 있는 매개변수 연습입니다. apply_discount(10000) == 9000
    """
    return int(price * (1 - rate))
