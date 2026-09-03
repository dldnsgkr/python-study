"""B9 · 리스트·딕셔너리 도구상자 — 반복을 짧게 만드는 것들

B3에서 리스트와 딕셔너리를 '만드는' 법을 배웠습니다. 여기서는 **다루는 도구**를 익힙니다.
이 도구들을 알면 5줄짜리 for 문이 1줄이 됩니다.

이번 파트에서 쓰는 도구:
    enumerate(xs)         (번호, 값) 을 함께 준다        for i, x in enumerate(xs)
    enumerate(xs, start=1) 1번부터 셀 때
    zip(a, b)             두 리스트를 나란히 묶는다
    d.items()             (키, 값) 쌍으로 순회
    d.keys() / d.values()
    sorted(xs, key=...)   기준을 정해 정렬
    sorted(xs, reverse=True)
    x in xs               들어 있는지 확인
"""

from __future__ import annotations

from typing import Any


def numbered(items: list[str]) -> list[str]:
    """번호를 붙인 문자열 리스트로 바꾼다. 번호는 1부터.

    numbered(["사과", "배"]) == ["1. 사과", "2. 배"]

    ⚠️ 직접 카운터 변수를 만들지 마세요. enumerate(items, start=1) 이 있습니다.
       `for i in range(len(items))` 도 파이썬답지 않은 습관입니다.
    """
    raise NotImplementedError


def pair_up(names: list[str], scores: list[int]) -> dict[str, int]:
    """두 리스트를 짝지어 딕셔너리로 만든다.

    pair_up(["김", "이"], [90, 80]) == {"김": 90, "이": 80}

    zip 은 두 리스트를 나란히 묶어 줍니다. 길이가 다르면 **짧은 쪽에 맞춰 조용히 잘립니다.**
    dict(zip(...)) 한 줄이면 끝납니다.
    """
    raise NotImplementedError


def invert(mapping: dict[str, int]) -> dict[int, str]:
    """키와 값을 뒤집은 딕셔너리를 만든다.

    invert({"김": 90, "이": 80}) == {90: "김", 80: "이"}

    d.items() 로 (키, 값) 을 함께 꺼내 순회하세요.
    값이 겹치면 나중 것이 이깁니다 — 그래서 뒤집기는 항상 안전한 연산이 아닙니다.
    """
    raise NotImplementedError


def count_words(text: str) -> dict[str, int]:
    """단어가 몇 번 나오는지 센다. 공백으로 나누고 소문자로 통일.

    count_words("a b a") == {"a": 2, "b": 1}
    count_words("") == {}

    딕셔너리에 누적하는 가장 기본 패턴입니다:
        counts[word] = counts.get(word, 0) + 1
    .get(키, 기본값) 은 "없으면 기본값"이라 첫 등장도 자연스럽게 처리됩니다.
    """
    raise NotImplementedError


def top_two(scores: list[int]) -> list[int]:
    """가장 큰 두 개를 내림차순으로. 두 개가 안 되면 있는 만큼.

    top_two([70, 95, 80]) == [95, 80]
    top_two([10]) == [10]

    sorted(xs, reverse=True) 로 정렬한 뒤 슬라이싱 [:2] 하세요.
    ⚠️ xs.sort() 는 원본을 바꿉니다. sorted(xs) 는 새 리스트를 줍니다. 여기선 후자를.
    """
    raise NotImplementedError


def rank_names(students: list[dict[str, Any]]) -> list[str]:
    """점수가 높은 순으로 이름만 뽑는다. 동점이면 먼저 나온 사람이 앞.

    rank_names([{"name": "김", "score": 80}, {"name": "이", "score": 95}]) == ["이", "김"]

    sorted 의 key 에 "무엇을 기준으로 정렬할지"를 함수로 줍니다:
        sorted(students, key=lambda s: s["score"], reverse=True)
    lambda 는 이름 없는 짧은 함수입니다. `lambda s: s["score"]` 는
    "s 를 받아 s['score'] 를 돌려주는 함수"라는 뜻입니다.
    """
    raise NotImplementedError


def remove_all(xs: list[Any], value: Any) -> list[Any]:
    """해당 값을 **전부** 없앤 새 리스트를 돌려준다. 원본은 그대로.

    remove_all([1, 2, 1, 3], 1) == [2, 3]

    ⚠️ list.remove() 는 **첫 번째 하나만** 지웁니다. 그리고 원본을 바꿉니다.
       순회하면서 지우면 원소를 건너뛰는 버그가 생깁니다(코어 08에서 다시 만납니다).
       조건에 맞는 것만 새 리스트에 담는 쪽이 언제나 안전합니다.
    """
    raise NotImplementedError


def flatten_once(nested: list[list[Any]]) -> list[Any]:
    """한 겹만 펼친다.

    flatten_once([[1, 2], [3], []]) == [1, 2, 3]

    힌트: 빈 리스트를 만들고 for 로 돌면서 extend 하세요.
          append 는 '하나를 붙이고', extend 는 '여러 개를 이어 붙입니다'.
    """
    raise NotImplementedError


def has_duplicate(xs: list[Any]) -> bool:
    """중복이 있는지 확인한다.

    has_duplicate([1, 2, 1]) is True
    has_duplicate([1, 2, 3]) is False

    힌트: set 은 중복을 없앱니다. 길이를 비교해 보세요. 한 줄로 됩니다.
    """
    raise NotImplementedError
