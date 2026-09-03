"""정답 비교와 실제 실행 — 퀴즈 러너와 검증 테스트가 함께 씁니다."""

from __future__ import annotations

import io
import re
from contextlib import redirect_stdout

from quiz.questions import Question


def normalize(text: str) -> str:
    """공백·따옴표·대소문자 차이를 무시하고 비교하기 위한 정규화.

    [1, 2, 4] 와 [1,2,4] 를, 'a' 와 "a" 를 같은 것으로 봅니다.
    개념을 맞혔는지가 중요하지 띄어쓰기를 맞혔는지가 중요한 게 아니니까요.
    """
    text = text.strip().replace("'", '"')
    return re.sub(r"\s+", "", text).lower()


def is_correct(question: Question, given: str) -> bool:
    candidates = {question.answer, *question.accept}
    return normalize(given) in {normalize(c) for c in candidates}


def run(question: Question) -> str:
    """문제의 코드를 실제로 실행해 결과를 돌려준다.

    kind="output" 이면 표준출력, kind="raises" 면 발생한 예외의 클래스 이름.
    """
    buffer = io.StringIO()
    namespace: dict[str, object] = {"__name__": "__quiz__"}
    try:
        with redirect_stdout(buffer):
            exec(compile(question.code, f"<quiz {question.id}>", "exec"), namespace)
    except Exception as exc:
        if question.kind != "raises":
            raise
        return type(exc).__name__
    if question.kind == "raises":
        raise AssertionError(f"{question.id}: 예외가 날 줄 알았는데 나지 않았습니다")
    return buffer.getvalue().rstrip("\n")
