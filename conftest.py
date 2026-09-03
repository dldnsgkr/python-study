"""테스트가 어떤 코드를 채점할지 정하고, 채점 결과를 요약해 준다.

기본값은 src/ (당신이 채우는 스켈레톤).
STUDY_SOLUTIONS=1 로 실행하면 solutions/ (모범답안)을 채점한다 — 문제 자체가
풀 수 있는 상태인지 확인할 때만 쓰세요.
"""

from __future__ import annotations

import os
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent
BASE = ROOT / ("solutions" if os.environ.get("STUDY_SOLUTIONS") else "src")
sys.path.insert(0, str(BASE))

_PART_ORDER = ["basics", "kit", "extra", "backend", "capstone", "quiz"]
_PART_LABEL = {
    "basics": "기초 B1~B15",
    "kit": "코어 01~19",
    "extra": "확장 드릴",
    "backend": "백엔드 B1~B4",
    "capstone": "캡스톤 A",
    "quiz": "퀴즈 데이터",
}


def _pad(text: str, width: int) -> str:
    """터미널에서 보이는 '칸 수' 기준으로 오른쪽 패딩.

    한글은 한 글자가 두 칸이라 f"{s:<12}" 로 맞추면 표가 어긋납니다.
    (확장 드릴 03번 pad_display 와 같은 문제입니다)
    """
    visual = sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in text)
    return text + " " * max(0, width - visual)


def _sort_key(report) -> tuple[int, str, int]:
    """학습 순서(기초 → 코어 → 확장 → 백엔드 → 캡스톤) → 파일 → 줄 번호."""
    part = _part_of(report.nodeid)
    order = _PART_ORDER.index(part) if part in _PART_ORDER else len(_PART_ORDER)
    return order, report.location[0], report.location[1] or 0


def _part_of(nodeid: str) -> str:
    if nodeid.startswith("capstone/"):
        return "capstone"
    if nodeid.startswith("quiz/"):
        return "quiz"
    for part in _PART_ORDER:
        if nodeid.startswith(f"tests/{part}/"):
            return part
    return "기타"


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    stats = terminalreporter.stats
    passed = stats.get("passed", [])
    failed = stats.get("failed", []) + stats.get("error", [])
    total = len(passed) + len(failed)
    if not total:
        return

    write = terminalreporter.write_line
    write("")

    # -x 로 첫 실패에서 멈췄다면 전체 진행률은 의미가 없다 — 다음 할 일만 알려준다
    if config.getoption("maxfail", default=0) == 1:      # -x 로 첫 실패에서 멈춘 경우
        first = min(failed, key=_sort_key)
        write(f"  다음 문제 →  {first.nodeid}")
        write("  전체 진행률은  ./study  로 확인하세요.")
        return

    by_part: dict[str, list[int]] = {}
    for report in passed:
        by_part.setdefault(_part_of(report.nodeid), [0, 0])[0] += 1
    for report in failed:
        by_part.setdefault(_part_of(report.nodeid), [0, 0])[1] += 1

    for part in [*_PART_ORDER, "기타"]:
        if part not in by_part:
            continue
        ok, bad = by_part[part]
        sub_total = ok + bad
        pct = ok * 100 // sub_total
        bar = "█" * (pct // 5) + "·" * (20 - pct // 5)
        label = _PART_LABEL.get(part, part)
        write(f"  {_pad(label, 14)}{bar}  {ok:>3}/{sub_total:<3} ({pct}%)")

    pct = len(passed) * 100 // total
    bar = "█" * (pct // 5) + "·" * (20 - pct // 5)
    write("  " + "─" * 46)
    write(f"  {_pad('전체', 14)}{bar}  {len(passed):>3}/{total:<3} ({pct}%)")

    skipped = stats.get("skipped", [])
    if any(r.nodeid.startswith("tests/backend/") for r in skipped):
        write("")
        write("  백엔드 트랙은 건너뛰었습니다 →  ./study backend  (라이브러리를 알아서 설치합니다)")

    if not failed:
        write("")
        write("  전부 통과했습니다. README의 다음 단계로 넘어가세요.")
        return

    errors = stats.get("error", [])
    if errors:
        write("")
        write(f"  ERROR {len(errors)}건 — 아직 구현하지 않은 함수를 테스트 준비 단계에서")
        write("  불렀다는 뜻입니다. 고장이 아니니 그냥 순서대로 채워 나가세요.")

    first = min(failed, key=_sort_key)
    write("")
    write(f"  다음 문제 →  {first.nodeid}")
    write(f"  이것만 다시 채점:  uv run pytest '{first.nodeid}'")
