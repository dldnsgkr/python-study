"""퀴즈 문제 은행 검증.

**틀린 정답이 들어 있는 퀴즈는 안 배우느니만 못합니다.**
그래서 모든 문제의 코드를 실제로 실행해 정답과 대조합니다.
학생용 채점(`./study`)에는 포함되지 않고 `./study verify` 에서만 돕니다.
"""

import pytest
from quiz.checker import is_correct, normalize, run
from quiz.questions import QUESTIONS


@pytest.mark.parametrize("question", QUESTIONS, ids=lambda q: q.id)
def test_answer_matches_actual_execution(question):
    actual = run(question)
    assert normalize(actual) == normalize(question.answer), (
        f"{question.id}: 적어 둔 정답 {question.answer!r} 과 "
        f"실제 실행 결과 {actual!r} 가 다릅니다"
    )


@pytest.mark.parametrize("question", QUESTIONS, ids=lambda q: q.id)
def test_accepted_alternatives_also_pass(question):
    assert is_correct(question, question.answer)
    for alternative in question.accept:
        assert is_correct(question, alternative), f"{question.id}: {alternative!r} 이 거부됨"


def test_ids_are_unique():
    ids = [q.id for q in QUESTIONS]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("question", QUESTIONS, ids=lambda q: q.id)
def test_every_question_explains_why(question):
    assert question.explain.strip(), f"{question.id}: 설명이 없습니다"
    assert question.doc, f"{question.id}: 관련 문서가 없습니다"
