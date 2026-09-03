"""B15 · 타입 힌트 — 이 워크북 전체가 쓰는 문법

지금까지 본 모든 스켈레톤에 `name: str` 이나 `-> int` 가 붙어 있었습니다.
그게 뭔지 여기서 배웁니다. 코어 15파트와 백엔드 트랙 전체가 이것 위에 서 있습니다.

    def greet(name: str, times: int = 1) -> str:
             ^^^^^^^^^  ^^^^^^^^^^^^^^     ^^^
             인자 타입   기본값 있는 인자    반환 타입

읽는 법:
    str, int, float, bool, None       기본 타입
    list[int]                         정수들의 리스트
    dict[str, int]                    키가 문자열, 값이 정수인 딕셔너리
    tuple[str, int]                   (문자열, 정수) 정확히 두 개짜리 튜플
    int | None                        정수이거나 None ("Optional" 이라고도 부릅니다)
    str | int                         둘 중 하나

⚠️ **타입 힌트는 런타임에 아무 일도 하지 않습니다.**
   `def f(x: int)` 에 문자열을 넘겨도 파이썬은 그냥 실행합니다.
   힌트는 (1) 사람이 읽으라고, (2) mypy 같은 검사기가 읽으라고, (3) 에디터가 읽으라고
   있는 것입니다. TypeScript 처럼 컴파일 단계에서 막아 주지 않습니다.

   검사는 따로 돌립니다:   ./study types
"""

from __future__ import annotations

from typing import Any


def repeat(text, times=2):
    """문자열을 times 번 이어 붙인다.

    repeat("ab") == "abab"
    repeat("ab", 3) == "ababab"

    ✍️ **타입 힌트를 직접 붙이세요.** 지금 시그니처에는 힌트가 없습니다.
       text 는 문자열, times 는 정수, 돌려주는 것도 문자열입니다:
           def repeat(text: str, times: int = 2) -> str:
       기본값이 있는 인자는 `이름: 타입 = 기본값` 순서로 씁니다.
       (테스트가 실제로 힌트가 붙었는지 확인합니다)
    """
    raise NotImplementedError


def first_or_none(xs):
    """첫 원소. 비었으면 None.

    ✍️ 힌트를 직접 붙이세요. xs 는 정수 리스트, 반환은 정수이거나 None 입니다.

    first_or_none([1, 2]) == 1
    first_or_none([]) is None

    `int | None` 은 "정수이거나 없거나"입니다. 이걸 적어 두면 호출한 쪽이
    None 검사를 잊지 않습니다. 예전 문법 Optional[int] 와 같은 뜻입니다.
    """
    raise NotImplementedError


def count_lengths(words):
    """단어를 키로, 길이를 값으로.

    ✍️ 힌트를 직접 붙이세요. 안에 뭐가 들었는지까지 적어야 합니다.

    count_lengths(["a", "bcd"]) == {"a": 1, "bcd": 3}

    `dict[str, int]` 처럼 **안에 뭐가 들었는지**까지 적는 게 요점입니다.
    그냥 `dict` 라고만 쓰면 검사기가 도와줄 수 있는 게 거의 없습니다.
    """
    raise NotImplementedError


def parse_pair(text):
    """"이름:숫자" 를 (이름, 숫자) 로 나눈다.

    ✍️ 힌트를 직접 붙이세요. 반환은 (문자열, 정수) 정확히 두 개짜리 튜플입니다.

    parse_pair("age:30") == ("age", 30)
    형식이 안 맞으면 ValueError.

    `tuple[str, int]` 는 **정확히 두 개**이고 순서대로 문자열·정수라는 뜻입니다.
    개수가 정해지지 않은 튜플은 `tuple[int, ...]` 로 씁니다.
    """
    raise NotImplementedError


def to_int(value: str | float | bool) -> int:
    """정수로 바꾼다.

    to_int("42") == 42
    to_int(3.9) == 3          # 버림 (반올림이 아닙니다)
    to_int(True) == 1
    to_int("abc")  ->  ValueError

    파이썬의 타입 변환은 함수 호출입니다: int(x), str(x), float(x), bool(x), list(x)
    JS 의 암묵적 변환("1" + 1 == "11")과 달리 파이썬은 섞으면 TypeError 를 냅니다.
    """
    raise NotImplementedError


def describe_all(items: list[Any]) -> list[str]:
    """각 원소를 "타입:값" 으로 설명한다.

    describe_all([1, "a", True, None, 1.5]) == \\
        ["int:1", "str:a", "bool:True", "NoneType:None", "float:1.5"]

    ⚠️ True 를 int 로 판정하면 안 됩니다. bool 은 int 의 서브클래스라
       isinstance(True, int) 가 True 입니다. type(x).__name__ 을 쓰면 정확합니다.
    """
    raise NotImplementedError


def safe_len(value: str | list[Any] | dict[str, Any] | None) -> int:
    """길이를 돌려준다. None 이면 0.

    safe_len("abc") == 3
    safe_len([1, 2]) == 2
    safe_len({"a": 1}) == 1
    safe_len(None) == 0

    여러 타입을 받되 None 을 따로 처리하는 패턴입니다.
    `if value is None: return 0` 을 먼저 두면, 그 아래에서 검사기는
    value 가 None 이 아님을 압니다 — 이걸 '좁히기(narrowing)'라고 합니다.
    """
    raise NotImplementedError
