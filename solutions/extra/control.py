"""확장 06 모범답안."""

from __future__ import annotations

import hashlib
from typing import Any


class UserError(Exception):
    def __init__(self, status: int, message: str = "") -> None:
        super().__init__(message or f"user error: {status}")
        self.status = status


def route(response: dict) -> Any:
    match response:
        case {"status": 200 | 201, "body": body}:
            return body
        case {"status": int(status)} if 400 <= status < 500:
            raise UserError(status)
        case {"status": int(status)} if 500 <= status < 600:
            return "retry"
        case _:
            return "logged"


def sha256_of(path: str, chunk_size: int = 4096) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()
