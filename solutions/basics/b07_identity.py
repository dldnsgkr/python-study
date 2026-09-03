"""B7 모범답안."""

from __future__ import annotations


def compare(a: object, b: object) -> tuple[bool, bool]:
    return a == b, a is b


def alias_and_append(xs: list[int], value: int) -> tuple[list[int], list[int]]:
    alias = xs                # 복사가 아니라 같은 객체에 이름 하나를 더 붙인 것
    alias.append(value)
    return xs, alias


def average_score(students: list[dict[str, object]]) -> float:
    if not students:
        raise ValueError("학생이 없습니다")
    total = 0
    for student in students:
        total += int(student["score"])  # type: ignore[call-overload]
    return total / len(students)


def top_student(students: list[dict[str, object]]) -> str:
    if not students:
        raise ValueError("학생이 없습니다")
    best = max(students, key=lambda s: s["score"])  # type: ignore[return-value,arg-type]
    return str(best["name"])
