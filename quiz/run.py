"""예측 퀴즈 러너.

    ./study quiz              아직 못 맞힌 문제부터
    ./study quiz 04           특정 파트만  (04, 시퀀스, 예외 ... 부분 일치)
    ./study quiz review       전에 틀린 것만
    ./study quiz reset        진도 초기화
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from quiz.checker import is_correct
from quiz.questions import QUESTIONS, Question

PROGRESS_PATH = Path(__file__).parent / ".progress.json"

DIM = "\033[2m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
OFF = "\033[0m"


def load_progress() -> dict[str, list[str]]:
    if not PROGRESS_PATH.exists():
        return {"correct": [], "wrong": []}
    try:
        data = json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"correct": [], "wrong": []}
    return {"correct": data.get("correct", []), "wrong": data.get("wrong", [])}


def save_progress(progress: dict[str, list[str]]) -> None:
    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def indent(text: str, prefix: str = "   ") -> str:
    return "\n".join(prefix + line for line in text.splitlines())


def ask(question: Question, position: str) -> bool | None:
    """한 문제를 묻는다. True/False = 정답 여부, None = 그만두기."""
    print()
    print(f"{DIM}{'─' * 62}{OFF}")
    print(f" {CYAN}{position}{OFF}   {question.part}   {DIM}{question.doc}{OFF}")
    print()
    print(indent(question.code))
    print()

    prompt = "예외 이름은?" if question.kind == "raises" else "출력은?"
    print(f" {BOLD}{prompt}{OFF}  {DIM}(엔터=모르겠음, q=그만){OFF}")
    try:
        given = input(" > ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None

    if given.lower() in {"q", "quit", "exit"}:
        return None

    correct = bool(given) and is_correct(question, given)
    print()
    if correct:
        print(f" {GREEN}맞았습니다{OFF}")
    else:
        shown = question.answer.replace("\n", "\n           ")
        print(f" {RED}아닙니다{OFF}   정답: {BOLD}{shown}{OFF}")
    print()
    print(indent(question.explain, "   "))
    return correct


def pick(argument: str | None, progress: dict[str, list[str]]) -> list[Question]:
    if argument == "review":
        wrong = set(progress["wrong"])
        return [q for q in QUESTIONS if q.id in wrong]
    if argument:
        needle = argument.lower()
        return [q for q in QUESTIONS if needle in q.part.lower() or q.id.startswith(needle)]
    done = set(progress["correct"])
    remaining = [q for q in QUESTIONS if q.id not in done]
    return remaining or QUESTIONS      # 다 맞혔으면 처음부터 다시


def main(argv: list[str]) -> int:
    argument = argv[0] if argv else None

    if argument == "reset":
        PROGRESS_PATH.unlink(missing_ok=True)
        print("진도를 초기화했습니다.")
        return 0

    progress = load_progress()
    questions = pick(argument, progress)

    if not questions:
        if argument == "review":
            print("다시 볼 문제가 없습니다. 좋은 신호네요.")
        else:
            print(f"'{argument}' 에 해당하는 문제가 없습니다.")
            print("파트: " + ", ".join(sorted({q.part for q in QUESTIONS})))
        return 0

    print()
    print(f" {BOLD}예측 퀴즈{OFF} — 실행하기 전에 읽고 맞히세요. {len(questions)}문제.")
    print(f" {DIM}AI가 짜 준 코드를 검토하려면 '읽고 맞히는' 능력이 필요합니다.{OFF}")

    asked = correct_count = 0
    for index, question in enumerate(questions, start=1):
        result = ask(question, f"{index}/{len(questions)}")
        if result is None:
            break
        asked += 1
        correct_count += result

        if result:
            if question.id not in progress["correct"]:
                progress["correct"].append(question.id)
            if question.id in progress["wrong"]:
                progress["wrong"].remove(question.id)
        else:
            if question.id not in progress["wrong"]:
                progress["wrong"].append(question.id)
            if question.id in progress["correct"]:
                progress["correct"].remove(question.id)
        save_progress(progress)

    print()
    print(f"{DIM}{'─' * 62}{OFF}")
    if asked:
        pct = correct_count * 100 // asked
        bar = "█" * (pct // 5) + "·" * (20 - pct // 5)
        print(f"  {bar}  {correct_count}/{asked} ({pct}%)")
    total_done = len(set(progress["correct"]))
    print(f"  전체 진도  {total_done}/{len(QUESTIONS)}")
    if progress["wrong"]:
        print(f"  틀린 {len(progress['wrong'])}문제 다시 보기:  ./study quiz review")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
