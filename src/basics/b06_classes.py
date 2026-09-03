"""B6 · 클래스 — 나만의 데이터 종류 만들기   (docs/07_basics_B6.md)"""

from __future__ import annotations


class Person:
    """이름과 나이를 담고 자기소개를 돌려준다.

    p = Person("김파이", 25)
    p.name == "김파이" / p.age == 25
    p.introduce() == "저는 김파이이고 25살입니다"
    """

    def __init__(self, name: str, age: int) -> None:
        raise NotImplementedError

    def introduce(self) -> str:
        raise NotImplementedError


class BankAccount:
    """잔액을 담고 입금·출금하는 계좌.

    account = BankAccount(1000)
    account.deposit(500)   -> 1500 (잔액을 돌려준다)
    account.withdraw(200)  -> 1300

    ⚠️ 원본 워크북은 잔액이 모자라면 문자열 "잔액 부족" 을 돌려줬습니다.
       그러면 호출한 쪽이 숫자를 받았는지 문자열을 받았는지 매번 확인해야 하고,
       실수로 그냥 쓰면 조용히 망가집니다. 여기서는 예외를 내도록 바꿨습니다:
         - 잔액보다 많이 출금하면      ValueError("잔액 부족")
         - 0 이하 금액을 입금/출금하면 ValueError("금액은 0보다 커야 합니다")
    """

    def __init__(self, balance: int = 0) -> None:
        raise NotImplementedError

    def deposit(self, amount: int) -> int:
        raise NotImplementedError

    def withdraw(self, amount: int) -> int:
        raise NotImplementedError
