"""B3 · 여러 값 담기 — 리스트·튜플·딕셔너리·세트   (docs/04_basics_B3.md)"""

from __future__ import annotations


def add_food(foods: list[str], new_food: str) -> tuple[str, str]:
    """음식을 하나 추가한 뒤 (첫 번째, 마지막) 을 돌려준다.

    ⚠️ 원본 리스트 foods 는 그대로 두어야 합니다.
       리스트에 append 하면 원본이 바뀝니다 — 새 리스트를 만들어 쓰세요.
       (B7에서 다룰 '같은 객체를 두 이름이 가리킨다' 문제의 예고편입니다)
    """
    new_list = foods + [new_food]
    return new_list[0], new_list[-1]


def profile_lines(profile: dict[str, object]) -> list[str]:
    """딕셔너리를 "키: 값" 문장 리스트로 바꾼다.

    {"이름": "김파이", "나이": 25} -> ["이름: 김파이", "나이: 25"]
    순서는 딕셔너리에 넣은 순서 그대로여야 합니다.
    """
    list_of_strings = []
    for key, value in profile.items():
        list_of_strings.append(key + ": " + str(value))
    return list_of_strings


def unique_sorted(numbers: list[int]) -> list[int]:
    """중복을 없애고 오름차순으로 정렬한 리스트를 돌려준다.

    세트(set)를 거치면 중복이 사라집니다. 다만 세트는 순서가 없으니
    다시 리스트로 만들고 정렬해야 합니다.
    """
    return sorted(set(numbers))


def add_hobby(profile: dict[str, object], hobby: str) -> dict[str, object]:
    """취미를 추가한 '새' 딕셔너리를 돌려준다. 원본은 건드리지 않는다."""
    return {**profile, "취미": hobby}


def has_key(profile: dict[str, object], key: str) -> bool:
    """키가 있는지 `in` 으로 확인한다."""
    return key in profile
