"""CAPSTONE A — 로그 분석 CLI.

각 함수의 NotImplementedError 를 지우고 구현하세요.
자세한 요구사항은 옆의 README.md 를 보세요.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from datetime import datetime
from enum import IntEnum
from pathlib import Path


class StatusClass(IntEnum):
    """상태 코드의 큰 분류. 200 → OK, 404 → CLIENT_ERROR 처럼 묶는 데 씁니다."""

    INFO = 1
    OK = 2
    REDIRECT = 3
    CLIENT_ERROR = 4
    SERVER_ERROR = 5

    @classmethod
    def of(cls, status: int) -> StatusClass:
        """상태 코드 정수를 분류로 바꾼다. 404 -> StatusClass.CLIENT_ERROR"""
        raise NotImplementedError


class ParseError(Exception):
    """한 줄을 해석하지 못했을 때. 전체를 중단시키지 않고 모아 두었다가 요약합니다.

    line_no 와 raw(원본 줄) 를 속성으로 갖습니다.
    """

    def __init__(self, line_no: int, raw: str, reason: str = "") -> None:
        super().__init__(f"{line_no}행 파싱 실패: {reason or raw[:60]}")
        self.line_no = line_no
        self.raw = raw


class Entry:
    """로그 한 줄. **frozen dataclass** 로 만드세요.

        ip: str, when: datetime, method: str, path: str, status: int, bytes_sent: int

    frozen 인 이유: 집계 도중 누가 값을 바꾸면 결과를 믿을 수 없게 됩니다.
    """


class Report:
    """집계 결과. 이것도 **frozen dataclass** 로.

        total: int                       전체 건수
        by_class: dict[StatusClass, int] 상태 분류별 건수
        bytes_total: int                 전송 바이트 합
        top_paths: list[tuple[str, int]] 요청 많은 경로 상위 5개 (내림차순)
    """


def parse_line(line: str, line_no: int) -> Entry:
    """Common Log Format 한 줄을 Entry 로. 형식이 다르면 ParseError.

    127.0.0.1 - - [24/Jul/2026:10:00:00 +0900] "GET /a HTTP/1.1" 200 512

    시각은 timezone 정보를 살려 aware datetime 으로 만드세요 (16파트).
    힌트: datetime.strptime(..., "%d/%b/%Y:%H:%M:%S %z") 는 로케일 영향을 받습니다.
          월 이름 표는 직접 두는 편이 안전합니다.
    """
    raise NotImplementedError


def read_lines(paths: Iterable[str | Path]) -> Iterator[tuple[int, str]]:
    """여러 파일을 이어 (전체 줄번호, 줄) 로 흘려보낸다. 빈 줄은 건너뛴다.

    ⚠️ f.readlines() 나 리스트 누적을 쓰지 마세요. 그 순간 파일 크기만큼 메모리를 씁니다.
    """
    raise NotImplementedError


def parse(numbered_lines: Iterable[tuple[int, str]]) -> Iterator[Entry | ParseError]:
    """줄을 Entry 로 바꾸되, 실패한 줄은 **예외를 던지지 말고 ParseError 객체를 내보낸다**.

    한 줄이 깨졌다고 10GB 짜리 분석을 통째로 날릴 수는 없으니까요.
    실패를 '값'으로 다루면 파이프라인이 끝까지 흐르고, 마지막에 요약할 수 있습니다.
    """
    raise NotImplementedError


def filter_entries(
    entries: Iterable[Entry],
    *,
    since: datetime | None = None,
    status: int | None = None,
) -> Iterator[Entry]:
    """조건에 맞는 Entry 만 통과시킨다. 조건이 None 이면 그 조건은 적용하지 않는다.

    since 는 **이상**(>=) 으로 비교합니다.
    """
    raise NotImplementedError


def aggregate(entries: Iterable[Entry]) -> Report:
    """Entry 스트림을 한 번만 훑어 Report 를 만든다.

    ⚠️ list(entries) 로 받아 두면 스트리밍의 의미가 없어집니다. 한 번의 for 로 끝내세요.
    top_paths 는 건수 내림차순 상위 5개. 동점이면 처음 나온 경로가 앞.
    """
    raise NotImplementedError


def build_report(
    paths: Iterable[str | Path],
    *,
    since: datetime | None = None,
    status: int | None = None,
) -> tuple[Report, list[ParseError]]:
    """네 단계를 연결하고, 파싱 실패 목록을 함께 돌려준다.

    이 함수 몸통은 몇 줄이면 됩니다. 그게 파이프라인 설계의 이점입니다.
    """
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """CLI 진입점.

    여기부터는 테스트가 없습니다 — argparse 로 직접 만들어 보세요.
      --since 2026-07-24        그 시각 이후만
      --status 200              그 상태 코드만
      --format text|json        출력 형식
    파일이 여러 개면 ProcessPoolExecutor 로 병렬 처리하는 것까지가 원문 요구사항입니다.
    """
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
