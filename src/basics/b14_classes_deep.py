"""B14 · 클래스 더 깊이 — 상속·특수 메서드·property

B6에서 클래스를 만드는 법을 배웠습니다. 여기서는 클래스로 할 수 있는 나머지를 봅니다.

이번 파트에서 쓰는 도구:
    class Dog(Animal):        상속 — Animal 의 것을 물려받는다
    super().__init__(...)     부모의 것을 부른다
    def speak(self):          같은 이름으로 다시 정의하면 '오버라이드'
    __str__ / __repr__        사람이 보는 문자열 / 개발자가 보는 문자열
    __eq__                    == 의 뜻을 정한다
    클래스 변수               모든 인스턴스가 **공유**한다
    @property                 메서드를 속성처럼 쓰게 한다
    @classmethod              첫 인자가 클래스 — 대체 생성자에 쓴다
    @staticmethod             self 도 cls 도 안 받는, 그냥 묶어 둔 함수
    isinstance(x, Animal)     이 타입인지 확인
"""

from __future__ import annotations


class Animal:
    """모든 동물의 부모 클래스.

    - __init__(self, name: str) 이 name 을 저장한다
    - speak(self) -> str 은 "{name}: ..." 를 돌려준다 (기본은 "{name}: ...")
    - **클래스 변수** count 로 지금까지 만들어진 동물 수를 센다
      (인스턴스가 아니라 클래스에 붙어 모두가 공유합니다.
       __init__ 안에서 Animal.count += 1 로 올리세요 — self.count += 1 이 아닙니다.
       self.count += 1 은 인스턴스에 새 속성을 만들어 버려서 공유가 깨집니다)

    Animal.reset_count() 로 0으로 되돌릴 수 있어야 합니다 (@classmethod).
    """

    count = 0


class Dog(Animal):
    """Animal 을 상속한다.

    Dog("바둑이").speak() == "바둑이: 멍멍"
    Dog("바둑이", breed="진돗개").breed == "진돗개"

    - __init__ 에서 **super().__init__(name)** 을 불러 부모의 초기화를 재사용하세요.
      직접 self.name = name 이라고 써도 지금은 되지만, 부모가 바뀌면 따라가지 않습니다.
    - breed 는 키워드 인자, 기본값은 "믹스"
    - speak 를 오버라이드해 "멍멍" 을 돌려주세요
    """


class Cat(Animal):
    """Cat("나비").speak() == "나비: 야옹" — speak 만 오버라이드하면 됩니다."""


class Point:
    """좌표. 특수 메서드를 연습합니다.

    p = Point(1, 2)
    str(p) == "(1, 2)"                  ← __str__ : 사람이 읽는 형태
    repr(p) == "Point(1, 2)"            ← __repr__ : 개발자가 보는 형태(디버깅·로그)
    Point(1, 2) == Point(1, 2)          ← __eq__ : 값이 같으면 같다
    Point(1, 2) != Point(3, 4)

    Point.from_string("1,2") == Point(1, 2)     ← @classmethod, 대체 생성자
    Point.distance(Point(0,0), Point(3,4)) == 5.0   ← @staticmethod

    __repr__ 만 정의하면 __str__ 은 자동으로 그걸 씁니다. 하나만 만들 거면 __repr__ 을.

    @classmethod 는 첫 인자로 **클래스 자신(cls)** 을 받습니다.
    그래서 `return cls(x, y)` 라고 쓰면 상속한 클래스에서도 알아서 맞는 타입이 나옵니다.
    """


class Rectangle:
    """직사각형. @property 를 연습합니다.

    r = Rectangle(3, 4)
    r.area == 12          ← 괄호 없이! 메서드가 아니라 속성처럼 씁니다
    r.width = 5           ← setter 가 검증합니다
    r.area == 20          ← width 를 바꾸면 area 도 따라 바뀝니다

    r.width = -1          ← ValueError("너비는 0보다 커야 합니다: -1")

    - area 는 **읽기 전용** property 입니다 (r.area = 10 은 AttributeError)
    - width 는 getter 와 setter 를 둘 다 가진 property 입니다
      실제 값은 self._width 에 저장하세요 (앞의 밑줄은 "내부용"이라는 관례입니다)

    ⚠️ area 를 __init__ 에서 계산해 필드로 저장하면 안 됩니다.
       width 를 바꿔도 따라가지 않으니까요. property 는 **읽을 때마다** 계산합니다.
    """

    def __init__(self, width: float, height: float) -> None:
        raise NotImplementedError


def describe(animal: Animal) -> str:
    """동물을 설명한다.

    describe(Dog("바둑이")) == "개 바둑이"
    describe(Cat("나비")) == "고양이 나비"
    describe(Animal("무명")) == "동물 무명"

    isinstance(x, Dog) 로 타입을 확인하세요.

    ⚠️ isinstance 는 **상속까지 봅니다** — isinstance(Dog("x"), Animal) 도 True 입니다.
       그래서 좁은 타입(Dog, Cat)을 먼저 검사하고 넓은 타입(Animal)을 나중에 봐야 합니다.
       순서를 뒤집으면 전부 "동물" 이 됩니다.
       (type(x) == Dog 는 상속을 무시합니다. 대개 isinstance 가 맞습니다)
    """
    raise NotImplementedError
