"""B10 · 반복의 도구 — while · break · continue · 컴프리헨션

B4에서 `for x in 리스트` 를 배웠습니다. 여기서는 나머지 반복 도구를 익힙니다.

이번 파트에서 쓰는 도구:
    while 조건:            조건이 참인 동안 계속
    break                  루프를 즉시 빠져나온다
    continue               이번 회차만 건너뛰고 다음으로
    range(시작, 끝, 걸음)   3번째 인자는 몇 칸씩 건너뛸지
    [식 for x in xs]              리스트 컴프리헨션
    [식 for x in xs if 조건]      거르면서 만들기
    {k: v for ...}                딕셔너리 컴프리헨션
"""

from __future__ import annotations


def countdown(n: int) -> list[int]:
    """n 부터 1까지 세어 내려간 리스트. n 이 0 이하면 빈 리스트.

    countdown(3) == [3, 2, 1]

    이번엔 **while 로** 만들어 보세요. 카운터 변수를 직접 줄여 나갑니다.
    ⚠️ while 은 조건이 거짓이 되게 만들어 주지 않으면 영원히 돕니다.
       루프 안에서 n 을 줄이는 걸 빠뜨리면 프로그램이 멈추지 않습니다(Ctrl+C 로 중단).
    """
    raise NotImplementedError


def first_negative(numbers: list[int]) -> int | None:
    """첫 음수를 돌려준다. 없으면 None.

    first_negative([3, -1, -5]) == -1
    first_negative([1, 2]) is None

    찾는 순간 **더 볼 이유가 없습니다.** break(또는 return)로 즉시 멈추세요.
    100만 개 중 첫 번째에서 찾았는데 끝까지 도는 코드가 의외로 흔합니다.
    """
    raise NotImplementedError


def skip_comments(lines: list[str]) -> list[str]:
    """빈 줄과 '#' 으로 시작하는 줄을 뺀 나머지를 돌려준다. 앞뒤 공백은 제거.

    skip_comments(["a", "", "# 주석", "  b  "]) == ["a", "b"]

    continue 로 "이번 줄은 건너뛰고 다음" 을 표현해 보세요.
    if 를 중첩해 오른쪽으로 밀려나는 것보다 읽기 쉽습니다.
    """
    raise NotImplementedError


def every_nth(start: int, end: int, step: int) -> list[int]:
    """start 부터 end 미만까지 step 칸씩.

    every_nth(0, 10, 3) == [0, 3, 6, 9]

    range 의 세 번째 인자입니다. range(끝) / range(시작, 끝) / range(시작, 끝, 걸음)
    셋 다 되고, 끝은 **포함하지 않습니다.**
    """
    raise NotImplementedError


def all_pairs(xs: list[str]) -> list[tuple[str, str]]:
    """서로 다른 두 원소의 모든 조합. 순서는 앞에서부터.

    all_pairs(["a", "b", "c"]) == [("a", "b"), ("a", "c"), ("b", "c")]

    반복문 안에 반복문을 넣습니다. 안쪽 루프의 시작을 바깥 인덱스+1 로 두면
    (a,b) 와 (b,a) 가 겹치지 않습니다.
    """
    raise NotImplementedError


def squares(numbers: list[int]) -> list[int]:
    """각 수의 제곱.

    squares([1, 2, 3]) == [1, 4, 9]

    **리스트 컴프리헨션**을 쓰세요:  [x * x for x in numbers]
    "빈 리스트 만들고 for 돌면서 append" 세 줄이 한 줄이 됩니다.
    파이썬 코드를 읽을 때 가장 자주 보게 될 문법입니다.
    """
    raise NotImplementedError


def long_words(words: list[str], min_length: int) -> list[str]:
    """길이가 min_length 이상인 단어만.

    long_words(["a", "abc", "abcd"], 3) == ["abc", "abcd"]

    컴프리헨션 뒤에 if 를 붙이면 거르면서 만듭니다:
        [w for w in words if 조건]
    """
    raise NotImplementedError


def word_lengths(words: list[str]) -> dict[str, int]:
    """단어를 키로, 길이를 값으로.

    word_lengths(["a", "abc"]) == {"a": 1, "abc": 3}

    **딕셔너리 컴프리헨션**입니다:  {w: len(w) for w in words}
    대괄호 대신 중괄호를 쓰고 `키: 값` 형태로 적습니다.
    """
    raise NotImplementedError
