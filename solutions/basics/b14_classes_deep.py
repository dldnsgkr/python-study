"""B14 모범답안."""

from __future__ import annotations

import math


class Animal:
    count = 0

    def __init__(self, name: str) -> None:
        self.name = name
        Animal.count += 1       # self.count += 1 이면 인스턴스 속성이 생겨 공유가 깨진다

    def speak(self) -> str:
        return f"{self.name}: ..."

    @classmethod
    def reset_count(cls) -> None:
        Animal.count = 0


class Dog(Animal):
    def __init__(self, name: str, *, breed: str = "믹스") -> None:
        super().__init__(name)  # 부모의 초기화를 재사용
        self.breed = breed

    def speak(self) -> str:
        return f"{self.name}: 멍멍"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name}: 야옹"


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    @classmethod
    def from_string(cls, text: str) -> Point:
        x, _, y = text.partition(",")
        return cls(int(x), int(y))      # cls 라 상속한 클래스에서도 맞는 타입이 나온다

    @staticmethod
    def distance(a: Point, b: Point) -> float:
        return math.hypot(a.x - b.x, a.y - b.y)


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width          # setter 를 거치므로 검증이 적용된다
        self.height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"너비는 0보다 커야 합니다: {value}")
        self._width = value

    @property
    def area(self) -> float:
        return self._width * self.height    # 읽을 때마다 계산 — 항상 최신


def describe(animal: Animal) -> str:
    if isinstance(animal, Dog):         # 좁은 타입부터 검사한다
        return f"개 {animal.name}"
    if isinstance(animal, Cat):
        return f"고양이 {animal.name}"
    return f"동물 {animal.name}"
