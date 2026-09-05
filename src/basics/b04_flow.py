"""B4 · 흐름 제어 — 조건과 반복   (docs/05_basics_B4.md)"""

from __future__ import annotations


def sign(n: int) -> str:
    """"양수" / "음수" / "0" 중 하나를 돌려준다. if / elif / else 연습."""
    if n > 0:
        return "양수"
    elif n < 0:
        return "음수"
    else:
        return "0"


def times_table(n: int) -> list[str]:
    """구구단 n 단을 문장 리스트로 만든다.

    times_table(2)[0] == "2 x 1 = 2"
    times_table(2)[8] == "2 x 9 = 18"     (1~9단, 총 9줄)
    """
    return [f"{n} x {i} = {n * i}" for i in range(1, 10)]


def sum_to(n: int) -> int:
    """1부터 n 까지의 합. n 이 0 이하면 0.

    for 로 한 번, 그다음 sum(range(...)) 로 한 번 — 두 가지로 짜 보세요.
    """
    if n <= 0:
        return 0
    else:
        return sum(range(1, n + 1))


def bigger_than(numbers: list[int], threshold: int) -> list[int]:
    """threshold 보다 큰 수만 순서대로 모아 돌려준다."""
    return [n for n in numbers if n > threshold]


def grade(score: int) -> str:
    """점수를 학점으로. 90+ A, 80+ B, 70+ C, 그 미만 F.

    ⚠️ 0~100 을 벗어난 점수는 ValueError 를 내세요.
       "잘못된 입력은 조용히 통과시키지 말 것" — 이게 이 문제의 진짜 주제입니다.
    """
    if score < 0 or score > 100:
        raise ValueError("점수는 0~100 사이여야 합니다.")
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"
