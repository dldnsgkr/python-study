"""CAPSTONE A 모범답안."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import IntEnum
from pathlib import Path

LINE_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<ts>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+)(?: [^"]*)?" '
    r'(?P<status>\d{3}) (?P<bytes>\d+|-)\s*$'
)

MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


class StatusClass(IntEnum):
    INFO = 1
    OK = 2
    REDIRECT = 3
    CLIENT_ERROR = 4
    SERVER_ERROR = 5

    @classmethod
    def of(cls, status: int) -> StatusClass:
        return cls(status // 100)


class ParseError(Exception):
    def __init__(self, line_no: int, raw: str, reason: str = "") -> None:
        super().__init__(f"{line_no}행 파싱 실패: {reason or raw[:60]}")
        self.line_no = line_no
        self.raw = raw


@dataclass(frozen=True)
class Entry:
    ip: str
    when: datetime
    method: str
    path: str
    status: int
    bytes_sent: int


@dataclass(frozen=True)
class Report:
    total: int = 0
    by_class: dict[StatusClass, int] = field(default_factory=dict)
    bytes_total: int = 0
    top_paths: list[tuple[str, int]] = field(default_factory=list)


def _parse_timestamp(raw: str) -> datetime:
    stamp, _, offset = raw.partition(" ")
    day, month, rest = stamp.split("/", 2)
    year, hour, minute, second = rest.split(":")
    sign = -1 if offset.startswith("-") else 1
    delta = timedelta(hours=int(offset[1:3]), minutes=int(offset[3:5]))
    return datetime(
        int(year), MONTHS[month], int(day), int(hour), int(minute), int(second),
        tzinfo=timezone(sign * delta),
    )


def parse_line(line: str, line_no: int) -> Entry:
    match = LINE_PATTERN.match(line.strip())
    if match is None:
        raise ParseError(line_no, line, "형식 불일치")
    try:
        when = _parse_timestamp(match["ts"])
    except (KeyError, ValueError) as exc:
        raise ParseError(line_no, line, f"시각 해석 실패: {exc}") from exc
    raw_bytes = match["bytes"]
    return Entry(
        ip=match["ip"],
        when=when,
        method=match["method"],
        path=match["path"],
        status=int(match["status"]),
        bytes_sent=0 if raw_bytes == "-" else int(raw_bytes),
    )


def read_lines(paths: Iterable[str | Path]) -> Iterator[tuple[int, str]]:
    line_no = 0
    for path in paths:
        with open(path, encoding="utf-8") as f:
            for raw in f:                      # 한 줄씩 — 파일 크기와 메모리가 무관하다
                line_no += 1
                if raw.strip():
                    yield line_no, raw.rstrip("\n")


def parse(numbered_lines: Iterable[tuple[int, str]]) -> Iterator[Entry | ParseError]:
    for line_no, line in numbered_lines:
        try:
            yield parse_line(line, line_no)
        except ParseError as exc:
            yield exc                          # 실패를 '값'으로 흘려보낸다


def filter_entries(
    entries: Iterable[Entry],
    *,
    since: datetime | None = None,
    status: int | None = None,
) -> Iterator[Entry]:
    for entry in entries:
        if since is not None and entry.when < since:
            continue
        if status is not None and entry.status != status:
            continue
        yield entry


def aggregate(entries: Iterable[Entry]) -> Report:
    total = 0
    bytes_total = 0
    by_class: Counter[StatusClass] = Counter()
    paths: Counter[str] = Counter()
    for entry in entries:                      # 단 한 번의 순회
        total += 1
        bytes_total += entry.bytes_sent
        by_class[StatusClass.of(entry.status)] += 1
        paths[entry.path] += 1
    return Report(
        total=total,
        by_class=dict(by_class),
        bytes_total=bytes_total,
        top_paths=paths.most_common(5),
    )


def build_report(
    paths: Iterable[str | Path],
    *,
    since: datetime | None = None,
    status: int | None = None,
) -> tuple[Report, list[ParseError]]:
    errors: list[ParseError] = []

    def entries_only(stream: Iterable[Entry | ParseError]) -> Iterator[Entry]:
        for item in stream:
            if isinstance(item, ParseError):
                errors.append(item)
            else:
                yield item

    report = aggregate(
        filter_entries(entries_only(parse(read_lines(paths))), since=since, status=status)
    )
    return report, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="접근 로그 분석")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--since", type=datetime.fromisoformat, default=None)
    parser.add_argument("--status", type=int, default=None)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    report, errors = build_report(args.paths, since=args.since, status=args.status)

    if args.format == "json":
        print(json.dumps({
            "total": report.total,
            "by_class": {k.name: v for k, v in report.by_class.items()},
            "bytes_total": report.bytes_total,
            "top_paths": report.top_paths,
            "parse_errors": len(errors),
        }, ensure_ascii=False, indent=2))
    else:
        print(f"전체 {report.total}건, {report.bytes_total:,} 바이트")
        for status_class, count in sorted(report.by_class.items()):
            print(f"  {status_class.name:<13} {count}")
        print("상위 경로")
        for path, count in report.top_paths:
            print(f"  {path:<24} {count}")
        if errors:
            print(f"파싱 실패 {len(errors)}건 (첫 줄: {errors[0].line_no}행)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
