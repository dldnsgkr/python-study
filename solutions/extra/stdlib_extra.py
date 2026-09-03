"""확장 16 모범답안."""

from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Iterable
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

LOG_PATTERN = re.compile(
    r"^\[(?P<level>[A-Z]+)\]\s+(?P<timestamp>\S+)\s+(?P<message>.*)$"
)


def count_by_extension(root: str | Path) -> dict[str, tuple[int, int]]:
    counts: Counter[str] = Counter()
    sizes: Counter[str] = Counter()
    for path in Path(root).rglob("*"):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        counts[ext] += 1
        sizes[ext] += path.stat().st_size
    return {ext: (counts[ext], sizes[ext]) for ext in counts}


def parse_log_line(line: str) -> dict[str, str] | None:
    match = LOG_PATTERN.match(line.strip())
    return match.groupdict() if match else None


def count_levels(lines: Iterable[str]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for line in lines:
        parsed = parse_log_line(line)
        if parsed is not None:
            counter[parsed["level"]] += 1
    return dict(counter)


def _encode(obj: Any) -> dict[str, str]:
    if isinstance(obj, datetime):
        return {"__type__": "datetime", "value": obj.isoformat()}
    if isinstance(obj, Decimal):
        return {"__type__": "Decimal", "value": str(obj)}
    raise TypeError(f"직렬화할 수 없는 타입: {type(obj).__name__}")


def _decode(d: dict[str, Any]) -> Any:
    match d:
        case {"__type__": "datetime", "value": str(value)}:
            return datetime.fromisoformat(value)
        case {"__type__": "Decimal", "value": str(value)}:
            return Decimal(value)
    return d


def dumps_rich(obj: Any) -> str:
    return json.dumps(obj, default=_encode, ensure_ascii=False)


def loads_rich(s: str) -> Any:
    return json.loads(s, object_hook=_decode)
