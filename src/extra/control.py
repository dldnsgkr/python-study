"""확장 06 — 제어 흐름   (docs/15_core_06.md DRILL 06)"""

from __future__ import annotations

from typing import Any


class UserError(Exception):
    """4xx 응답을 나타내는 도메인 예외. status 속성에 상태 코드를 담는다."""

    def __init__(self, status: int, message: str = "") -> None:
        super().__init__(message or f"user error: {status}")
        self.status = status


def route(response: dict) -> Any:
    """HTTP 응답 dict를 `match` 문으로 분기한다.

    {"status": 200, "body": X} 또는 {"status": 201, ...}  -> X 를 반환
    4xx (400~499)                                        -> UserError(status) 발생
    5xx (500~599)                                        -> 문자열 "retry" 반환
    그 외                                                -> 문자열 "logged" 반환

    if/elif 로도 되지만 이번엔 match 의 매핑 패턴을 써 보세요:
        match response:
            case {"status": 200 | 201, "body": body}: ...
    """
    raise NotImplementedError


def sha256_of(path: str, chunk_size: int = 4096) -> str:
    """파일을 chunk_size 바이트씩 읽어 SHA-256 16진 문자열을 만든다.

    파일 전체를 read() 로 올리면 큰 파일에서 메모리가 터집니다.
    walrus 연산자로 "읽고 → 비었는지 보고 → 처리" 를 한 줄에 담아 보세요:
        while chunk := f.read(chunk_size):
    """
    raise NotImplementedError
