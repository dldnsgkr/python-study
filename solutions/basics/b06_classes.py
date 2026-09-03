"""B6 모범답안."""

from __future__ import annotations


class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def introduce(self) -> str:
        return f"저는 {self.name}이고 {self.age}살입니다"


class BankAccount:
    def __init__(self, balance: int = 0) -> None:
        self.balance = balance

    def deposit(self, amount: int) -> int:
        if amount <= 0:
            raise ValueError("금액은 0보다 커야 합니다")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: int) -> int:
        if amount <= 0:
            raise ValueError("금액은 0보다 커야 합니다")
        if amount > self.balance:
            raise ValueError("잔액 부족")
        self.balance -= amount
        return self.balance
