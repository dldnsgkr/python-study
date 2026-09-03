"""확장 15 — 타입   (docs/24_core_15.md DRILL 15)

이 파일은 `uv run mypy src/extra/typed.py` 로도 채점됩니다.
"""

from __future__ import annotations

from typing import overload

STORE: dict[str, str] = {"a": "1"}


@overload
def get(key: str) -> str | None: ...
@overload
def get(key: str, default: str) -> str: ...


def get(key: str, default: str | None = None) -> str | None:
    """STORE 에서 값을 꺼낸다.

    위의 @overload 선언이 말하는 것:
      - default 를 안 주면 없을 수도 있으니 `str | None`
      - default 를 주면 항상 값이 있으니 `str`
    호출한 쪽에서 불필요한 None 검사를 안 해도 되게 만드는 게 목적입니다.

    구현은 한 줄입니다. @overload 선언부는 이미 써 뒀으니 몸통만 채우세요.
    """
    raise NotImplementedError


class Repository:
    """Protocol 로 정의할 리포지터리 인터페이스 — 는 아래에 직접 만드세요.

    docs/24_core_15.md 의 3번 문제입니다.
    typing.Protocol 을 상속한 `RepositoryProto` 를 정의하고,
    이 클래스가 **상속 없이도** 그 타입으로 통과하는지 mypy 로 확인하세요.
    (런타임 테스트로는 확인할 수 없는, 타입 검사기만이 잡아 주는 것이 요점입니다)
    """

    def get(self, key: str) -> str | None:
        return STORE.get(key)
