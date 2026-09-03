"""확장 15 모범답안."""

from __future__ import annotations

from typing import Protocol, overload

STORE: dict[str, str] = {"a": "1"}


@overload
def get(key: str) -> str | None: ...
@overload
def get(key: str, default: str) -> str: ...


def get(key: str, default: str | None = None) -> str | None:
    return STORE.get(key, default)


class RepositoryProto(Protocol):
    """구조적 타이핑 — 상속 없이 '모양'만 맞으면 이 타입이다."""

    def get(self, key: str) -> str | None: ...


class Repository:
    def get(self, key: str) -> str | None:
        return STORE.get(key)


def _typecheck(repo: RepositoryProto) -> str | None:
    """Repository 는 RepositoryProto 를 상속하지 않지만 mypy가 통과시킨다."""
    return repo.get("a")


_ = _typecheck(Repository())
