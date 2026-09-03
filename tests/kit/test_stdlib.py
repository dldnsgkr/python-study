"""코어 16 · 19 채점."""

from datetime import UTC, date, datetime, timedelta

from kit.stdlib import day_range_utc, dedupe


class TestDayRangeUtc:
    def test_seoul_day_starts_at_15_utc_previous_day(self):
        start, end = day_range_utc(date(2026, 7, 24), "Asia/Seoul")
        assert start == datetime(2026, 7, 23, 15, 0, tzinfo=UTC)
        assert end == datetime(2026, 7, 24, 15, 0, tzinfo=UTC)

    def test_is_half_open_24h(self):
        start, end = day_range_utc(date(2026, 1, 1))
        assert end - start == timedelta(days=1)

    def test_returns_aware_datetimes(self):
        start, end = day_range_utc(date(2026, 1, 1))
        assert start.tzinfo is not None and end.tzinfo is not None

    def test_dst_transition_day_is_not_24h(self):
        # 미국 동부 서머타임 시작일은 23시간이다
        start, end = day_range_utc(date(2026, 3, 8), "America/New_York")
        assert end - start == timedelta(hours=23)

    def test_dst_end_day_is_25h(self):
        # 서머타임 종료일은 25시간이다 — "start + 24시간" 으로 짜면 여기서 걸린다
        start, end = day_range_utc(date(2026, 11, 1), "America/New_York")
        assert end - start == timedelta(hours=25)


class TestDedupe:
    def test_preserves_first_occurrence_order(self):
        assert dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]

    def test_empty(self):
        assert dedupe([]) == []

    def test_is_linear_not_quadratic(self):
        import time
        data = list(range(200_000)) * 2
        started = time.perf_counter()
        dedupe(data)
        assert time.perf_counter() - started < 1.0     # list `in` 을 쓰면 실패한다
