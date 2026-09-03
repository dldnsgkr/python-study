"""예측 퀴즈 문제 은행.

각 문제의 `code` 는 **실제로 실행 가능한** 코드이고, `answer` 는 그 실행 결과입니다.
quiz/tests/test_quiz_data.py 가 전부 실행해 정답이 맞는지 검증합니다 —
퀴즈에 틀린 정답이 들어 있으면 안 배우느니만 못하니까요.

kind:
    "output"  코드를 실행했을 때 표준출력
    "raises"  발생하는 예외의 클래스 이름
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Question:
    id: str
    part: str
    code: str
    answer: str
    explain: str
    doc: str = ""
    kind: str = "output"
    accept: tuple[str, ...] = field(default_factory=tuple)


QUESTIONS: list[Question] = [
    # ── 01 객체 모델 ────────────────────────────────────────
    Question(
        id="01-1",
        part="01 객체 모델",
        doc="docs/10_core_01.md",
        code="""a = ([1, 2], 3)
a[0].append(4)
print(a)""",
        answer="([1, 2, 4], 3)",
        explain=(
            "튜플의 불변성은 '들고 있는 참조가 고정'이라는 뜻이지, 참조가 가리키는 객체까지\n"
            "얼린다는 뜻이 아닙니다. 안의 리스트는 여전히 바뀝니다.\n"
            "그래서 가변 원소를 담은 튜플은 해시도 불가능합니다."
        ),
    ),
    Question(
        id="01-2",
        part="01 객체 모델",
        doc="docs/10_core_01.md",
        kind="raises",
        code="""a = ([1, 2], 3)
a[1] = 5""",
        answer="TypeError",
        explain="튜플은 __setitem__ 을 아예 구현하지 않습니다. '막는' 게 아니라 '없는' 것입니다.",
    ),
    Question(
        id="01-3",
        part="01 객체 모델",
        doc="docs/10_core_01.md",
        kind="raises",
        code="""x = "hello"
x[0] = "H\"""",
        answer="TypeError",
        explain=(
            "str 도 불변이라 아이템 대입 프로토콜이 없습니다.\n"
            "JS 도 문자열이 불변이지만 조용히 무시합니다 — 파이썬은 터뜨립니다."
        ),
    ),
    Question(
        id="01-4",
        part="01 객체 모델",
        doc="docs/08_basics_B7.md",
        code="""a = [1, 2]
b = a
b.append(3)
print(a)""",
        answer="[1, 2, 3]",
        explain="b = a 는 복사가 아니라 같은 객체에 이름 하나를 더 붙인 것입니다.",
    ),
    Question(
        id="01-5",
        part="01 객체 모델",
        doc="docs/08_basics_B7.md",
        code="""print([1, 2] == [1, 2], [1, 2] is [1, 2])""",
        answer="True False",
        explain="== 는 '값이 같은가', is 는 '아예 같은 객체인가'. 리스트 두 개는 별개의 객체입니다.",
    ),
    Question(
        id="01-6",
        part="01 객체 모델",
        doc="docs/16_core_07.md",
        code="""def add(item, target=[]):
    target.append(item)
    return target

print(add(1))
print(add(2))""",
        answer="[1]\n[1, 2]",
        accept=("[1] [1, 2]",),
        explain=(
            "기본값은 함수가 **정의될 때 한 번** 만들어져 함수 객체에 붙습니다(func.__defaults__).\n"
            "호출할 때마다 새로 만들어지지 않아서, 호출을 거듭할수록 같은 리스트에 쌓입니다.\n"
            "가변 기본값은 항상 None 으로 두고 함수 안에서 만드세요:\n"
            "    def add(item, target=None):\n"
            "        target = [] if target is None else target\n"
            "덧붙여, print(add(1), add(2)) 로 한 줄에 찍으면 '[1, 2] [1, 2]' 가 나옵니다 —\n"
            "둘 다 **같은 리스트 객체**를 가리키니까요."
        ),
    ),
    # ── 02 숫자 ─────────────────────────────────────────────
    Question(
        id="02-1",
        part="02 숫자",
        doc="docs/11_core_02.md",
        code="""print({1: "a", True: "b", 1.0: "c"})""",
        answer="{1: 'c'}",
        explain=(
            "1 == True == 1.0 이고 해시값도 같으므로 셋은 같은 키입니다.\n"
            "키 객체는 처음 것(1)이 남고 값만 마지막 것으로 덮어써집니다."
        ),
    ),
    Question(
        id="02-2",
        part="02 숫자",
        doc="docs/11_core_02.md",
        code="""print(0.1 + 0.2 == 0.3)""",
        answer="False",
        explain=(
            "0.1 과 0.2 는 이진 부동소수점으로 정확히 표현되지 않습니다.\n"
            "돈 계산에는 Decimal 을, 비교에는 math.isclose 를 쓰세요."
        ),
    ),
    Question(
        id="02-3",
        part="02 숫자",
        doc="docs/11_core_02.md",
        code="""print(7 // -2, 7 % -2)""",
        answer="-4 -1",
        explain=(
            "파이썬의 // 는 내림(floor)이고, % 의 부호는 **나누는 수**를 따릅니다.\n"
            "JS 는 잘라내기(trunc)라 7 / -2 | 0 은 -3, 7 % -2 는 1 입니다. 완전히 다릅니다."
        ),
    ),
    Question(
        id="02-4",
        part="02 숫자",
        doc="docs/11_core_02.md",
        code="""print(1 + True, sum([True, True, False]))""",
        answer="2 2",
        explain="bool 은 int 의 서브클래스입니다. True 는 그냥 1 입니다.",
    ),
    # ── 03 문자열 ───────────────────────────────────────────
    Question(
        id="03-1",
        part="03 문자열",
        doc="docs/12_core_03.md",
        code="""print("key=value=extra".split("=", 1))""",
        answer="['key', 'value=extra']",
        explain="두 번째 인자는 '최대 몇 번 나눌지'입니다. partition('=') 도 같은 결과를 줍니다.",
    ),
    Question(
        id="03-2",
        part="03 문자열",
        doc="docs/12_core_03.md",
        code="""print("abc"[::-1], "ab" * 3)""",
        answer="cba ababab",
        explain="슬라이스의 세 번째 값은 걸음(step)이고, 문자열 * 정수는 반복입니다.",
    ),
    Question(
        id="03-3",
        part="03 문자열",
        doc="docs/12_core_03.md",
        code="""print(len("커피"), len("커피".encode()))""",
        answer="2 6",
        explain=(
            "str 의 길이는 **문자 수**, bytes 의 길이는 **바이트 수**입니다.\n"
            "한글 한 글자는 UTF-8 에서 3바이트입니다. 그래서 바이트 스트림을 아무 데서나\n"
            "자르면 decode 가 깨집니다."
        ),
    ),
    # ── 04 시퀀스 ───────────────────────────────────────────
    Question(
        id="04-1",
        part="04 시퀀스",
        doc="docs/13_core_04.md",
        code="""xs = [1, 2, 3]
k = 0
print(xs[-k:])""",
        answer="[1, 2, 3]",
        explain=(
            "-0 은 그냥 0 이라 xs[-0:] 는 xs[0:] 가 되어 **전체**를 돌려줍니다.\n"
            "회전 함수를 짤 때 가장 자주 물리는 off-by-zero 함정입니다."
        ),
    ),
    Question(
        id="04-2",
        part="04 시퀀스",
        doc="docs/13_core_04.md",
        code="""xs = [1, 2, 3]
print(xs[5:])""",
        answer="[]",
        explain=(
            "인덱스는 범위를 벗어나면 IndexError 지만, **슬라이스는 조용히 잘라 냅니다.**\n"
            "빈 리스트가 나와서 버그를 늦게 발견하는 흔한 경로입니다."
        ),
    ),
    Question(
        id="04-3",
        part="04 시퀀스",
        doc="docs/13_core_04.md",
        code="""matrix = [[0] * 2] * 3
matrix[0][0] = 9
print(matrix)""",
        answer="[[9, 0], [9, 0], [9, 0]]",
        explain=(
            "* 3 은 **같은 리스트 객체의 참조를 3개** 만듭니다. 행 세 개가 전부 같은 객체입니다.\n"
            "제대로 만들려면 [[0] * 2 for _ in range(3)] 처럼 매번 새로 만드세요."
        ),
    ),
    Question(
        id="04-4",
        part="04 시퀀스",
        doc="docs/13_core_04.md",
        code="""print(list(zip([1, 2, 3], "ab")))""",
        answer="[(1, 'a'), (2, 'b')]",
        explain=(
            "zip 은 **가장 짧은 것에 맞춰** 조용히 잘립니다.\n"
            "길이가 같아야 한다면 zip(..., strict=True) 를 쓰세요(3.10+). 다르면 터집니다."
        ),
    ),
    # ── 05 매핑과 집합 ──────────────────────────────────────
    Question(
        id="05-1",
        part="05 매핑과 집합",
        doc="docs/14_core_05.md",
        code="""from collections import defaultdict

d = defaultdict(list)
if d["x"]:
    pass
print(dict(d))""",
        answer="{'x': []}",
        explain=(
            "defaultdict 는 **조회만 해도** 키를 만들어 버립니다(유령 키).\n"
            "그래서 group_by 같은 함수는 반환 전에 평범한 dict 로 바꿔야 합니다."
        ),
    ),
    Question(
        id="05-2",
        part="05 매핑과 집합",
        doc="docs/14_core_05.md",
        code="""d = {"a": 1}
print(d.get("b"), d.get("b", 0))""",
        answer="None 0",
        explain="d['b'] 는 KeyError 지만 .get 은 기본값(없으면 None)을 돌려줍니다.",
    ),
    Question(
        id="05-3",
        part="05 매핑과 집합",
        doc="docs/14_core_05.md",
        kind="raises",
        code="""class M:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

print(len({M(1), M(1)}))""",
        answer="TypeError",
        explain=(
            "__eq__ 를 정의하면 __hash__ 가 자동으로 None 이 됩니다 — 해시 불가.\n"
            "'같은 것은 같은 해시를 가져야 한다'는 규약을 파이썬이 강제하는 방식입니다.\n"
            "set/dict 에 넣으려면 __hash__ 도 같이 정의하세요."
        ),
    ),
    # ── 06 제어 흐름 ────────────────────────────────────────
    Question(
        id="06-1",
        part="06 제어 흐름",
        doc="docs/15_core_06.md",
        code="""fs = [lambda: i for i in range(3)]
print([f() for f in fs])""",
        answer="[2, 2, 2]",
        explain=(
            "람다는 i 의 **값이 아니라 이름**을 붙잡습니다(늦은 바인딩). 호출 시점의 i 는 2 입니다.\n"
            "JS 의 var 로 만든 클로저와 같은 문제입니다. 고치려면 기본 인자로 그 시점의 값을\n"
            "묶으세요:  [lambda i=i: i for i in range(3)]"
        ),
    ),
    Question(
        id="06-2",
        part="06 제어 흐름",
        doc="docs/15_core_06.md",
        code="""for x in [1, 2]:
    if x == 3:
        break
else:
    print("못 찾음")""",
        answer="못 찾음",
        explain=(
            "for-else 의 else 는 '루프가 break 없이 끝났을 때' 실행됩니다.\n"
            "'조건이 거짓일 때'가 아닙니다 — 이름이 헷갈리기로 유명합니다."
        ),
    ),
    Question(
        id="06-3",
        part="06 제어 흐름",
        doc="docs/15_core_06.md",
        code="""print(any([]), all([]))""",
        answer="False True",
        explain=(
            "빈 것에 대해 all 은 True 입니다(반증할 원소가 없으니까). 수학의 공허참입니다.\n"
            "'전부 유효한가' 검사에서 빈 목록이 통과해 버리는 버그의 원인입니다."
        ),
    ),
    Question(
        id="06-4",
        part="06 제어 흐름",
        doc="docs/03_basics_B2.md",
        code="""print(bool([]), bool("0"), bool(" "))""",
        answer="False True True",
        explain=(
            "JS 와 다릅니다. JS 에서 [] 는 truthy 지만 파이썬에서 빈 컬렉션은 전부 falsy 입니다.\n"
            '반대로 문자열 "0" 은 둘 다 truthy 이고, 공백 한 칸도 truthy 입니다.'
        ),
    ),
    # ── 07 함수 ─────────────────────────────────────────────
    Question(
        id="07-1",
        part="07 함수",
        doc="docs/16_core_07.md",
        code="""def outer():
    x = 1

    def inner():
        x = 2

    inner()
    return x

print(outer())""",
        answer="1",
        explain=(
            "inner 안의 x = 2 는 **새 지역 변수**를 만듭니다. 바깥 x 를 바꾸려면 nonlocal x 가 필요합니다.\n"
            "'대입하면 지역 변수'가 파이썬의 규칙입니다 — 읽기만 하면 바깥 것을 봅니다."
        ),
    ),
    Question(
        id="07-2",
        part="07 함수",
        doc="docs/16_core_07.md",
        code="""def f(a, b=[], *, c=1):
    pass

print(f.__defaults__, f.__kwdefaults__)""",
        answer="([],) {'c': 1}",
        explain=(
            "기본값이 함수 객체에 저장돼 있는 게 눈으로 보입니다.\n"
            "가변 기본값 버그(01-6)가 왜 생기는지가 여기서 설명됩니다."
        ),
    ),
    Question(
        id="07-3",
        part="07 함수",
        doc="docs/16_core_07.md",
        code="""def tag(name, *args, **kwargs):
    print(name, args, kwargs)

tag("a", 1, 2, href="x")""",
        answer="a (1, 2) {'href': 'x'}",
        explain="*args 는 튜플, **kwargs 는 dict 로 모입니다.",
    ),
    # ── 08 이터레이션 ───────────────────────────────────────
    Question(
        id="08-1",
        part="08 이터레이션",
        doc="docs/17_core_08.md",
        code="""g = (x for x in [1, 2, 3])
print(list(g), list(g))""",
        answer="[1, 2, 3] []",
        explain=(
            "제너레이터는 **한 번만** 소비됩니다. 두 번째 list() 는 이미 끝난 것을 읽어 빈 리스트입니다.\n"
            "리스트인 줄 알고 두 번 순회하는 버그가 조용히 생깁니다."
        ),
    ),
    Question(
        id="08-2",
        part="08 이터레이션",
        doc="docs/17_core_08.md",
        code="""xs = [1, 2, 3, 4]
for x in xs:
    if x % 2 == 0:
        xs.remove(x)
print(xs)""",
        answer="[1, 3]",
        explain=(
            "순회 중에 리스트를 바꾸면 인덱스가 밀려 원소를 **건너뜁니다.**\n"
            "2 를 지우자 3 이 그 자리로 당겨졌고, 다음 반복은 이미 다음 칸(4)을 봅니다.\n"
            "결과적으로 3 은 검사조차 되지 않았습니다 — 홀수라 살아남은 게 아니라 운이 좋았을 뿐입니다.\n"
            "새 리스트를 만드세요:  xs = [x for x in xs if x % 2]"
        ),
    ),
    Question(
        id="08-3",
        part="08 이터레이션",
        doc="docs/17_core_08.md",
        code="""from itertools import islice

print(list(islice(range(10), 2, 5)))""",
        answer="[2, 3, 4]",
        explain="islice 는 이터러블에 슬라이스를 적용합니다. 무한 제너레이터에도 쓸 수 있습니다.",
    ),
    # ── 10 클래스 ───────────────────────────────────────────
    Question(
        id="10-1",
        part="10 클래스",
        doc="docs/19_core_10.md",
        code="""class Dog:
    tricks = []

    def add(self, trick):
        self.tricks.append(trick)

a, b = Dog(), Dog()
a.add("구르기")
print(b.tricks)""",
        answer="['구르기']",
        explain=(
            "tricks 는 **클래스 변수**라 모든 인스턴스가 공유합니다.\n"
            "self.tricks.append 는 대입이 아니라 조회 후 변경이라 클래스 변수를 건드립니다.\n"
            "인스턴스마다 따로 두려면 __init__ 안에서 self.tricks = [] 로 만드세요."
        ),
    ),
    Question(
        id="10-2",
        part="10 클래스",
        doc="docs/19_core_10.md",
        code="""class A:
    x = 1

a = A()
a.x = 2
print(a.x, A.x)""",
        answer="2 1",
        explain=(
            "대입은 **인스턴스**에 새 속성을 만듭니다. 클래스 변수는 그대로입니다.\n"
            "조회는 인스턴스 → 클래스 순으로 찾고, 대입은 항상 인스턴스에 합니다."
        ),
    ),
    # ── 13 예외 ─────────────────────────────────────────────
    Question(
        id="13-1",
        part="13 예외",
        doc="docs/22_core_13.md",
        code="""def f():
    try:
        return "try"
    finally:
        print("finally")

print(f())""",
        answer="finally\ntry",
        accept=("finally try",),
        explain=(
            "finally 는 return 값이 정해진 **뒤, 실제로 돌아가기 전에** 실행됩니다.\n"
            "그래서 'finally' 가 먼저 찍히고 'try' 가 나중에 찍힙니다."
        ),
    ),
    Question(
        id="13-2",
        part="13 예외",
        doc="docs/22_core_13.md",
        kind="raises",
        code="""try:
    raise ValueError("문제")
except ValueError as e:
    pass

print(e)""",
        answer="NameError",
        explain=(
            "except ... as e 의 e 는 블록이 끝나면 **자동으로 삭제됩니다**(순환 참조 방지).\n"
            "밖에서 쓰려면 별도 변수에 담아 두세요:  err = e"
        ),
    ),
    Question(
        id="13-3",
        part="13 예외",
        doc="docs/22_core_13.md",
        code="""try:
    print(1 / 0)
except ArithmeticError:
    print("잡힘")""",
        answer="잡힘",
        explain=(
            "ZeroDivisionError 는 ArithmeticError 의 서브클래스입니다.\n"
            "예외도 계층이라 상위 클래스로 잡힙니다 — 도메인 예외에 뿌리를 하나 두는 이유입니다."
        ),
    ),
    # ── 16 표준 라이브러리 ──────────────────────────────────
    Question(
        id="16-1",
        part="16 표준 라이브러리",
        doc="docs/25_core_16.md",
        code="""import json

print(json.dumps({"이름": "김"}))""",
        answer='{"\\uc774\\ub984": "\\uae40"}',
        explain=(
            "json.dumps 는 기본이 ensure_ascii=True 라 한글이 이스케이프됩니다.\n"
            "로그·API 응답에서 한글이 깨져 보이면 대개 이것입니다. ensure_ascii=False 를 쓰세요."
        ),
    ),
    Question(
        id="16-2",
        part="16 표준 라이브러리",
        doc="docs/25_core_16.md",
        code="""from datetime import datetime

a = datetime(2026, 1, 1)
print(a.tzinfo)""",
        answer="None",
        explain=(
            "타임존 없이 만든 datetime 은 naive 입니다. 이걸 aware 와 비교하면 TypeError 가 나고,\n"
            "그냥 저장하면 '어느 지역의 시각인지 모르는 값'이 DB 에 쌓입니다.\n"
            "항상 datetime.now(UTC) 처럼 타임존을 붙이세요."
        ),
    ),
]
