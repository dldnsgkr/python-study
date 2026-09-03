"""B2 · 기본 데이터 타입 — 값의 종류   (docs/03_basics_B2.md)"""

from __future__ import annotations


def describe_type(value: object) -> str:
    """값의 타입 이름을 문자열로 돌려준다.

    describe_type(3) == "int" / describe_type("hi") == "str"
    힌트: type(value) 가 돌려주는 것도 하나의 객체이고, 이름을 갖고 있습니다.
    """
    return type(value).__name__


def greet(name: str, age: int) -> str:
    """f-문자열로 인사말을 만든다.

    greet("김파이", 25) == "김파이님은 25살입니다"
    """
    return name + "님은 " + str(age) + "살입니다"


def divide_report(a: int, b: int) -> tuple[float, int, int]:
    """(a / b, a // b, a % b) 세 결과를 한 번에 돌려준다.

    17 / 5, 17 // 5, 17 % 5 를 먼저 종이에 예상해 보고 실행하세요.
    """
    return a / b, a // b, a % b


def is_even(n: int) -> bool:
    """짝수면 True. `%` 를 써서 한 줄로 쓸 수 있습니다."""
    return n % 2 == 0


def sum_of_inputs(a: str, b: str) -> int:
    """사용자가 입력한 두 '문자열' 숫자의 합을 정수로 돌려준다.

    input() 은 언제나 문자열을 줍니다. 변환을 빼먹으면 "3" + "5" 가 "35" 가 되죠.
    이 함수는 그 변환 부분만 떼어낸 것입니다.
    """
    return int(a) + int(b)
