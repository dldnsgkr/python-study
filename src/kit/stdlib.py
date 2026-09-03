"""코어 16 · 19 — 표준 라이브러리 · 성능

docs/25_core_16.md, docs/28_core_19.md
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from datetime import date, datetime


# ── 16 표준 라이브러리 ─────────────────────────────────────
def day_range_utc(day: date, tz: str = "Asia/Seoul") -> tuple[datetime, datetime]:
    """해당 로컬 날짜의 [시작, 끝) 반열린 구간을 UTC aware datetime으로 반환한다.

    day_range_utc(date(2026, 7, 24), "Asia/Seoul")
        -> (2026-07-23 15:00 UTC, 2026-07-24 15:00 UTC)

    ⚠️ 23:59:59 로 끝을 잡으면 그 사이 1초를 놓칩니다. 항상 [start, end) 로.
    ⚠️ 서머타임이 있는 타임존에서는 하루가 23시간이나 25시간일 수 있습니다.
       "start + 24시간" 으로 끝을 구하면 그날 틀립니다.
       힌트: zoneinfo.ZoneInfo + datetime.combine(다음날, time.min)
    """
    raise NotImplementedError


# ── 19 성능 ────────────────────────────────────────────────
def dedupe(xs: Iterable[Hashable]) -> list:
    """순서를 유지하며 중복을 제거한다. O(n)이어야 한다.

    dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]
    함정: `if x not in result` 는 리스트 스캔이라 O(n²) 입니다. 40만 건이면 테스트가 안 끝납니다.
    """
    raise NotImplementedError
