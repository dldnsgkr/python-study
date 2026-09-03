"""CAPSTONE A 채점."""

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from analyzer import (
    Entry,
    ParseError,
    Report,
    StatusClass,
    aggregate,
    build_report,
    filter_entries,
    parse,
    parse_line,
    read_lines,
)

KST = timezone(timedelta(hours=9))
SAMPLE = Path(__file__).resolve().parent.parent / "sample.log"
GOOD = '127.0.0.1 - - [24/Jul/2026:10:00:00 +0900] "GET /index.html HTTP/1.1" 200 512'


class TestStatusClass:
    @pytest.mark.parametrize("status,expected", [
        (200, StatusClass.OK), (201, StatusClass.OK), (301, StatusClass.REDIRECT),
        (404, StatusClass.CLIENT_ERROR), (500, StatusClass.SERVER_ERROR),
    ])
    def test_of(self, status, expected):
        assert StatusClass.of(status) is expected


class TestParseLine:
    def test_fields(self):
        entry = parse_line(GOOD, 1)
        assert entry.ip == "127.0.0.1"
        assert entry.method == "GET"
        assert entry.path == "/index.html"
        assert entry.status == 200
        assert entry.bytes_sent == 512

    def test_timestamp_is_timezone_aware(self):
        entry = parse_line(GOOD, 1)
        assert entry.when == datetime(2026, 7, 24, 10, 0, 0, tzinfo=KST)
        assert entry.when.tzinfo is not None

    def test_dash_bytes_becomes_zero(self):
        line = '1.1.1.1 - - [24/Jul/2026:10:00:00 +0900] "GET / HTTP/1.1" 304 -'
        assert parse_line(line, 1).bytes_sent == 0

    @pytest.mark.parametrize("line", ["깨진 줄", "", "127.0.0.1 GET /"])
    def test_bad_line_raises_parse_error(self, line):
        with pytest.raises(ParseError) as info:
            parse_line(line, 42)
        assert info.value.line_no == 42

    def test_entry_is_frozen(self):
        import dataclasses
        entry = parse_line(GOOD, 1)
        assert dataclasses.is_dataclass(Entry)
        with pytest.raises(dataclasses.FrozenInstanceError):
            entry.status = 500


class TestReadLines:
    def test_numbers_lines_and_skips_blanks(self, tmp_path):
        p = tmp_path / "a.log"
        p.write_text("first\n\nsecond\n", encoding="utf-8")
        assert list(read_lines([p])) == [(1, "first"), (3, "second")]

    def test_numbering_continues_across_files(self, tmp_path):
        a, b = tmp_path / "a.log", tmp_path / "b.log"
        a.write_text("x\ny\n", encoding="utf-8")
        b.write_text("z\n", encoding="utf-8")
        assert [n for n, _ in read_lines([a, b])] == [1, 2, 3]

    def test_is_lazy(self, tmp_path):
        p = tmp_path / "a.log"
        p.write_text("\n".join(str(i) for i in range(100_000)), encoding="utf-8")
        stream = read_lines([p])
        assert next(stream) == (1, "0")       # 전부 읽고 시작하면 느려진다


class TestParse:
    def test_yields_errors_as_values_not_exceptions(self):
        items = list(parse([(1, GOOD), (2, "깨짐"), (3, GOOD)]))
        assert len(items) == 3
        assert isinstance(items[1], ParseError)
        assert isinstance(items[0], Entry)


class TestFilterEntries:
    def _entries(self):
        return [
            Entry("1.1.1.1", datetime(2026, 7, 24, 9, tzinfo=KST), "GET", "/a", 200, 10),
            Entry("1.1.1.1", datetime(2026, 7, 24, 11, tzinfo=KST), "GET", "/b", 404, 0),
        ]

    def test_no_filters_passes_everything(self):
        assert len(list(filter_entries(self._entries()))) == 2

    def test_since_is_inclusive(self):
        cutoff = datetime(2026, 7, 24, 9, tzinfo=KST)
        assert len(list(filter_entries(self._entries(), since=cutoff))) == 2

    def test_since_excludes_earlier(self):
        cutoff = datetime(2026, 7, 24, 10, tzinfo=KST)
        got = list(filter_entries(self._entries(), since=cutoff))
        assert [e.path for e in got] == ["/b"]

    def test_status(self):
        got = list(filter_entries(self._entries(), status=404))
        assert [e.path for e in got] == ["/b"]


class TestAggregate:
    def test_counts_bytes_and_classes(self):
        entries = [
            Entry("1", datetime(2026, 7, 24, tzinfo=KST), "GET", "/a", 200, 100),
            Entry("1", datetime(2026, 7, 24, tzinfo=KST), "GET", "/a", 200, 50),
            Entry("1", datetime(2026, 7, 24, tzinfo=KST), "GET", "/b", 500, 0),
        ]
        report = aggregate(entries)
        assert report.total == 3
        assert report.bytes_total == 150
        assert report.by_class == {StatusClass.OK: 2, StatusClass.SERVER_ERROR: 1}
        assert report.top_paths[0] == ("/a", 2)

    def test_empty(self):
        report = aggregate([])
        assert report.total == 0
        assert report.top_paths == []

    def test_top_paths_is_capped_at_five(self):
        entries = [
            Entry("1", datetime(2026, 7, 24, tzinfo=KST), "GET", f"/p{i}", 200, 0)
            for i in range(10)
        ]
        assert len(aggregate(entries).top_paths) == 5

    def test_consumes_a_generator_only_once(self):
        entries = (
            Entry("1", datetime(2026, 7, 24, tzinfo=KST), "GET", "/a", 200, 1)
            for _ in range(3)
        )
        assert aggregate(entries).total == 3

    def test_report_is_frozen(self):
        import dataclasses
        assert dataclasses.is_dataclass(Report)
        report = aggregate([])
        with pytest.raises(dataclasses.FrozenInstanceError):
            report.total = 99


class TestBuildReport:
    def test_end_to_end_on_the_sample_log(self):
        report, errors = build_report([SAMPLE])
        assert report.total == 7
        assert report.bytes_total == 2648
        assert report.by_class == {
            StatusClass.OK: 5,
            StatusClass.CLIENT_ERROR: 1,
            StatusClass.SERVER_ERROR: 1,
        }
        assert report.top_paths[0] == ("/index.html", 3)

    def test_parse_errors_are_collected_not_raised(self):
        _, errors = build_report([SAMPLE])
        assert len(errors) == 1
        assert errors[0].line_no == 5

    def test_filters_apply(self):
        report, _ = build_report([SAMPLE], status=200)
        assert report.total == 4
