"""확장 16 — 표준 라이브러리   (docs/25_core_16.md DRILL 16)"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any


def count_by_extension(root: str | Path) -> dict[str, tuple[int, int]]:
    """디렉터리를 재귀 탐색해 확장자별 (파일 개수, 총 바이트) 를 집계한다.

    {".py": (3, 1024), ".md": (1, 88), "": (1, 12)}
    - 확장자는 소문자로 통일 (".PY" 와 ".py" 는 같은 것)
    - 확장자가 없는 파일은 빈 문자열 "" 키
    - 디렉터리는 세지 않는다
    힌트: Path.rglob("*") 와 collections.Counter
    """
    raise NotImplementedError


def parse_log_line(line: str) -> dict[str, str] | None:
    """"[INFO] 2026-01-01T10:00:00 서버 시작" 형식을 파싱한다.

    -> {"level": "INFO", "timestamp": "2026-01-01T10:00:00", "message": "서버 시작"}
    형식에 안 맞으면 None.

    정규식에 **이름 있는 그룹** (?P<level>...) 을 쓰세요.
    group(1), group(2) 로 번호를 세다 보면 패턴이 바뀔 때마다 다 틀어집니다.
    """
    raise NotImplementedError


def count_levels(lines: Iterable[str]) -> dict[str, int]:
    """로그 줄들에서 레벨별 개수를 센다. 파싱 안 되는 줄은 무시.

    반환은 평범한 dict 여야 합니다(Counter 를 그대로 돌려줘도 == 는 통과하지만,
    05파트의 '유령 키' 문제를 떠올려 보세요).
    """
    raise NotImplementedError


def dumps_rich(obj: Any) -> str:
    """datetime 과 Decimal 이 섞인 객체를 JSON 문자열로 저장한다.

    기본 json 모듈은 이 둘을 모르기 때문에 TypeError 를 냅니다.
    타입 정보를 함께 남겨 loads_rich 가 원래 타입으로 되돌릴 수 있게 하세요.
    예: {"__type__": "datetime", "value": "2026-01-01T00:00:00+00:00"}
    힌트: json.dumps(obj, default=...) 와 json.loads(s, object_hook=...)
    """
    raise NotImplementedError


def loads_rich(s: str) -> Any:
    """dumps_rich 로 저장한 문자열을 원래 타입으로 복원한다.

    loads_rich(dumps_rich(x)) == x 가 성립해야 합니다(왕복 검증).
    """
    raise NotImplementedError
