"""B7 · == 와 is, 그리고 그다음   (docs/08_basics_B7.md)"""

from __future__ import annotations


def compare(a: object, b: object) -> tuple[bool, bool]:
    """(a == b, a is b) 를 돌려준다.

    == 는 "값이 같은가", is 는 "아예 같은 객체인가" 입니다.
    [1,2] == [1,2] 는 True 지만 is 는 False 인 이유를 말로 설명할 수 있어야 합니다.
    """
    return a == b, a is b


def alias_and_append(xs: list[int], value: int) -> tuple[list[int], list[int]]:
    """xs 에 다른 이름(별명)을 붙이고 그 별명으로 value 를 추가한다.

    (원본, 별명) 을 돌려주세요. 둘은 **같은 객체**라 내용이 함께 바뀝니다.
    복사본을 만들면 이 문제의 요점을 놓칩니다 — 일부러 같이 바뀌게 하세요.
    """
    
    xs_alias = xs  # xs 의 별명을 만들고
    xs_alias.append(value)  # 별명으로 value 를 추가합니다.
    return xs, xs_alias  # (원본, 별명) 을 돌려줍니다. 둘은 같은 객체라 내용이 함께 바뀝니다.


def average_score(students: list[dict[str, object]]) -> float:
    """[{"name": ..., "score": ...}, ...] 의 평균 점수.

    빈 리스트면 ValueError. 변수·리스트·딕셔너리·for·함수가 다 들어갑니다.
    """
    if students == []:
        raise ValueError("빈 리스트입니다.")
    
    return sum(student["score"] for student in students) / len(students)


def top_student(students: list[dict[str, object]]) -> str:
    """점수가 가장 높은 학생의 이름. 동점이면 먼저 나온 사람.

    max(..., key=...) 를 알아두면 한 줄입니다.
    """
    
    return max(students, key=lambda student: student["score"])["name"]
