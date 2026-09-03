"""코어 16 · 19 모범답안."""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo


def day_range_utc(day: date, tz: str = "Asia/Seoul") -> tuple[datetime, datetime]:
    zone = ZoneInfo(tz)
    start = datetime.combine(day, time.min, tzinfo=zone)
    end = datetime.combine(day + timedelta(days=1), time.min, tzinfo=zone)
    return start.astimezone(UTC), end.astimezone(UTC)


def dedupe(xs: Iterable[Hashable]) -> list:
    seen: set = set()
    out: list = []
    for x in xs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out
