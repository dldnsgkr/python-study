# KIT · 채점 키트 — 실습을 pytest로 검증하기

`solutions.py 를 채우고 초록불을 만드세요`

코어 트랙의 실습 중 **정답이 기계적으로 판정 가능한 것들**을 테스트로 옮겼습니다. 아래 파일을 그대로 만들고 `solutions.py`의 `NotImplementedError`를 하나씩 지워 나가세요. 전부 통과하면 코어 트랙의 핵심 개념을 손으로 구현한 셈이 됩니다.

*디렉터리*

```text
python-workbook-kit/
├── pyproject.toml
├── solutions.py            ← 당신이 채우는 유일한 파일
└── tests/
    ├── conftest.py
    ├── test_objects.py     # 01–05
    ├── test_functions.py   # 06–09
    ├── test_oop.py         # 10–13
    └── test_stdlib.py      # 14–19
```

*bash*

```bash
uv venv && source .venv/bin/activate
uv pip install pytest
pytest -q                       # 전체 채점
pytest -q tests/test_oop.py     # 파트별 채점
pytest -q -k rotate             # 문제 하나만
```

## solutions.py — 채워야 할 스켈레톤

*solutions.py*

```python
"""파이썬 워크북 실습 답안. 각 함수의 NotImplementedError를 지우고 구현하세요."""
from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable, Iterator, Sequence
from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

# ── 01 객체 모델 ────────────────────────────────────────────
def with_key(d: dict, path: list[str], value: Any) -> dict:
    """원본을 변경하지 않고 path 위치의 값을 바꾼 새 dict를 반환한다."""
    raise NotImplementedError

# ── 02 숫자 ────────────────────────────────────────────────
def total_with_vat(unit_price: str, qty: int) -> Decimal:
    """부가세 10%를 더한 총액을 1원 단위로 반올림(HALF_UP)해 반환한다."""
    raise NotImplementedError

# ── 03 문자열 ──────────────────────────────────────────────
def split_once(s: str, sep: str = "=") -> tuple[str, str]:
    """첫 구분자 기준으로만 두 조각으로 나눈다. 구분자가 없으면 (s, "")."""
    raise NotImplementedError

# ── 04 시퀀스 ──────────────────────────────────────────────
def rotate(xs: list, k: int) -> list:
    """오른쪽으로 k칸 회전한 새 리스트. k가 길이보다 커도 동작한다."""
    raise NotImplementedError

def flatten(xs: Iterable) -> list:
    """임의 깊이의 list/tuple을 평탄화한다. 문자열은 펼치지 않는다."""
    raise NotImplementedError

# ── 05 매핑과 집합 ─────────────────────────────────────────
def group_by(records: Iterable[Any], key: Callable[[Any], Hashable]) -> dict:
    raise NotImplementedError

def diff(old: dict, new: dict) -> dict:
    """{"added": {...}, "removed": {...}, "changed": {k: (old, new)}}"""
    raise NotImplementedError

# ── 06 제어 흐름 ───────────────────────────────────────────
def first_match(xs: Iterable, pred: Callable[[Any], bool], default=None):
    """조건을 만족하는 첫 원소. 없으면 default. 무한 이터러블에서도 즉시 반환."""
    raise NotImplementedError

def transpose(matrix: list[list]) -> list[list]:
    raise NotImplementedError

# ── 07 함수 ────────────────────────────────────────────────
def make_counter(start: int = 0) -> Callable[[], int]:
    """호출할 때마다 1씩 증가한 값을 반환하는 함수를 만든다(클로저)."""
    raise NotImplementedError

def bind_args(func: Callable, *args, **kwargs) -> dict:
    """호출 인자를 기본값까지 반영한 {이름: 값} dict로 정규화한다."""
    raise NotImplementedError

# ── 08 이터레이션 ──────────────────────────────────────────
def window(iterable: Iterable, n: int) -> Iterator[tuple]:
    """길이 n의 슬라이딩 윈도우. 원소가 n개 미만이면 아무것도 내지 않는다."""
    raise NotImplementedError

def batches(iterable: Iterable, size: int) -> Iterator[list]:
    """size개씩 묶어 낸다. 마지막 배치는 더 작을 수 있다."""
    raise NotImplementedError

# ── 09 데코레이터 ──────────────────────────────────────────
def retry(times: int = 3, exceptions: tuple[type[BaseException], ...] = (Exception,)):
    """실패 시 최대 times회까지 재시도하는 데코레이터. 메타데이터를 보존할 것."""
    raise NotImplementedError

# ── 10 클래스 ──────────────────────────────────────────────
class Temperature:
    """celsius를 저장하고 fahrenheit를 읽기/쓰기 가능한 property로 제공한다."""
    def __init__(self, celsius: float = 0.0) -> None:
        raise NotImplementedError

# ── 11 특수 메서드 ─────────────────────────────────────────
class Money:
    """같은 통화끼리만 +, 비교 가능. sum()도 동작해야 한다."""
    def __init__(self, amount: int, currency: str = "KRW") -> None:
        raise NotImplementedError

# ── 12 데이터 모델링 ───────────────────────────────────────
class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"

def transition(current: Status, nxt: Status) -> Status:
    """허용된 전이만 통과시키고, 아니면 ValueError를 낸다."""
    raise NotImplementedError

# ── 13 예외 ────────────────────────────────────────────────
class ConfigError(Exception):
    pass

def load_config(path: str) -> dict:
    """파일이 없으면 ConfigError로 변환하되 원인(__cause__)을 보존한다."""
    raise NotImplementedError

# ── 16 표준 라이브러리 ─────────────────────────────────────
def day_range_utc(day: date, tz: str = "Asia/Seoul") -> tuple[datetime, datetime]:
    """해당 로컬 날짜의 [시작, 끝) 반열린 구간을 UTC aware datetime으로 반환한다."""
    raise NotImplementedError

# ── 19 성능 ────────────────────────────────────────────────
def dedupe(xs: Iterable[Hashable]) -> list:
    """순서를 유지하며 중복을 제거한다. O(n)이어야 한다."""
    raise NotImplementedError
```

## tests/conftest.py — 점수 요약을 붙입니다

*tests/conftest.py*

```python
import pytest

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    errors = len(terminalreporter.stats.get("error", []))
    total = passed + failed + errors
    if not total:
        return
    pct = passed * 100 // total
    bar = "█" * (pct // 5) + "·" * (20 - pct // 5)
    terminalreporter.write_line("")
    terminalreporter.write_line(f"  채점  {bar}  {passed}/{total}  ({pct}%)")
    if pct == 100:
        terminalreporter.write_line("  전부 통과했습니다. 다음 트랙으로 넘어가세요.")
```

## tests/test_objects.py — 01~05

*tests/test_objects.py*

```python
from decimal import Decimal

import pytest

from solutions import (diff, flatten, group_by, rotate, split_once,
                       total_with_vat, with_key)

class TestWithKey:
    def test_returns_new_dict_without_touching_original(self):
        original = {"user": {"name": "kim", "age": 30}, "active": True}
        result = with_key(original, ["user", "name"], "lee")
        assert result["user"]["name"] == "lee"
        assert original["user"]["name"] == "kim"
        assert result["user"] is not original["user"]

    def test_creates_missing_intermediate_keys(self):
        assert with_key({}, ["a", "b"], 1) == {"a": {"b": 1}}

class TestTotalWithVat:
    @pytest.mark.parametrize("price,qty,expected", [
        ("19.99", 3, Decimal("66")),      # 59.97 * 1.1 = 65.967 → 66
        ("1000", 1, Decimal("1100")),
        ("0.05", 10, Decimal("1")),       # 0.5 * 1.1 = 0.55 → 1 (HALF_UP)
    ])
    def test_rounds_half_up(self, price, qty, expected):
        assert total_with_vat(price, qty) == expected

    def test_returns_decimal_not_float(self):
        assert isinstance(total_with_vat("100", 1), Decimal)

class TestSplitOnce:
    def test_splits_on_first_separator_only(self):
        assert split_once("key=value=extra") == ("key", "value=extra")

    def test_missing_separator(self):
        assert split_once("keyonly") == ("keyonly", "")

class TestRotate:
    @pytest.mark.parametrize("xs,k,expected", [
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
        ([1, 2, 3], 0, [1, 2, 3]),
        ([1, 2, 3], 3, [1, 2, 3]),
        ([1, 2, 3], 7, [3, 1, 2]),
        ([], 3, []),
    ])
    def test_rotate(self, xs, k, expected):
        assert rotate(xs, k) == expected

    def test_does_not_mutate_input(self):
        xs = [1, 2, 3]
        rotate(xs, 1)
        assert xs == [1, 2, 3]

class TestFlatten:
    def test_nested(self):
        assert flatten([1, [2, [3, [4]]], (5, 6)]) == [1, 2, 3, 4, 5, 6]

    def test_strings_are_not_exploded(self):
        assert flatten(["ab", ["cd"]]) == ["ab", "cd"]

class TestGroupBy:
    def test_groups_by_key(self):
        rows = [{"t": "a", "v": 1}, {"t": "b", "v": 2}, {"t": "a", "v": 3}]
        result = group_by(rows, lambda r: r["t"])
        assert set(result) == {"a", "b"}
        assert [r["v"] for r in result["a"]] == [1, 3]

    def test_returns_plain_dict_without_phantom_keys(self):
        result = group_by([], lambda r: r)
        assert result == {}
        result.get("missing")
        assert result == {}          # defaultdict를 그대로 반환하면 실패한다

class TestDiff:
    def test_added_removed_changed(self):
        old = {"a": 1, "b": 2, "c": 3}
        new = {"b": 2, "c": 30, "d": 4}
        result = diff(old, new)
        assert result["added"] == {"d": 4}
        assert result["removed"] == {"a": 1}
        assert result["changed"] == {"c": (3, 30)}
```

## tests/test_functions.py — 06~09

*tests/test_functions.py*

```python
from itertools import count

import pytest

from solutions import (batches, bind_args, first_match, make_counter, retry,
                       transpose, window)

class TestFirstMatch:
    def test_found(self):
        assert first_match([1, 3, 4, 6], lambda x: x % 2 == 0) == 4

    def test_default_when_missing(self):
        assert first_match([1, 3], lambda x: x > 100, default=-1) == -1

    def test_lazy_on_infinite_iterable(self):
        assert first_match(count(), lambda x: x > 5) == 6      # 무한 루프면 실패

class TestTranspose:
    def test_square_and_rect(self):
        assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]

    def test_empty(self):
        assert transpose([]) == []

class TestMakeCounter:
    def test_counts_up(self):
        c = make_counter()
        assert [c(), c(), c()] == [1, 2, 3]

    def test_counters_are_independent(self):
        a, b = make_counter(), make_counter(10)
        a()
        assert b() == 11

class TestBindArgs:
    def test_normalizes_positional_and_defaults(self):
        def f(a, b=2, *, c=3):
            ...
        assert bind_args(f, 1) == {"a": 1, "b": 2, "c": 3}
        assert bind_args(f, 1, 9, c=8) == {"a": 1, "b": 9, "c": 8}

class TestWindow:
    def test_sliding(self):
        assert list(window([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]

    def test_shorter_than_window(self):
        assert list(window([1], 3)) == []

    def test_yields_snapshots_not_live_buffer(self):
        got = list(window([1, 2, 3, 4], 2))
        assert got[0] == (1, 2)          # 버퍼를 그대로 yield하면 여기서 깨진다

    def test_lazy(self):
        assert next(window(count(), 3)) == (0, 1, 2)

class TestBatches:
    def test_last_batch_may_be_smaller(self):
        assert list(batches(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]]

    def test_empty(self):
        assert list(batches([], 3)) == []

class TestRetry:
    def test_retries_until_success(self):
        calls = []

        @retry(times=3, exceptions=(ValueError,))
        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise ValueError("아직")
            return "ok"

        assert flaky() == "ok"
        assert len(calls) == 3

    def test_reraises_after_exhausting(self):
        @retry(times=2, exceptions=(ValueError,))
        def always_fails():
            raise ValueError("끝까지 실패")

        with pytest.raises(ValueError, match="끝까지"):
            always_fails()

    def test_does_not_swallow_other_exceptions(self):
        @retry(times=3, exceptions=(ValueError,))
        def wrong_error():
            raise KeyError("다른 예외")

        with pytest.raises(KeyError):
            wrong_error()

    def test_preserves_metadata(self):
        @retry()
        def documented():
            """원본 docstring."""

        assert documented.__name__ == "documented"
        assert documented.__doc__ == "원본 docstring."
```

## tests/test_oop.py — 10~13

*tests/test_oop.py*

```python
import pytest

from solutions import ConfigError, Money, Status, Temperature, load_config, transition

class TestTemperature:
    def test_conversion_both_ways(self):
        t = Temperature(100)
        assert t.fahrenheit == pytest.approx(212)
        t.fahrenheit = 32
        assert t.celsius == pytest.approx(0)

    def test_fahrenheit_is_a_property_not_a_stored_field(self):
        assert isinstance(type(Temperature()).__dict__["fahrenheit"], property)

class TestMoney:
    def test_add_same_currency(self):
        assert (Money(1000) + Money(500)).amount == 1500

    def test_reject_different_currency(self):
        with pytest.raises(TypeError):
            Money(1000, "KRW") + Money(10, "USD")

    def test_comparison_and_sorting(self):
        xs = sorted([Money(300), Money(100), Money(200)])
        assert [m.amount for m in xs] == [100, 200, 300]

    def test_sum_works(self):
        assert sum([Money(100), Money(200)]).amount == 300

    def test_equality_and_hash(self):
        assert Money(100) == Money(100)
        assert len({Money(100), Money(100), Money(200)}) == 2

    def test_repr_is_informative(self):
        assert "100" in repr(Money(100))

class TestTransition:
    def test_allowed(self):
        assert transition(Status.PENDING, Status.PAID) is Status.PAID

    @pytest.mark.parametrize("cur,nxt", [
        (Status.PAID, Status.PENDING),
        (Status.CANCELED, Status.PAID),
    ])
    def test_rejected(self, cur, nxt):
        with pytest.raises(ValueError):
            transition(cur, nxt)

class TestLoadConfig:
    def test_wraps_and_preserves_cause(self, tmp_path):
        missing = tmp_path / "nope.json"
        with pytest.raises(ConfigError) as info:
            load_config(str(missing))
        assert isinstance(info.value.__cause__, FileNotFoundError)

    def test_reads_valid_file(self, tmp_path):
        p = tmp_path / "config.json"
        p.write_text('{"debug": true}', encoding="utf-8")
        assert load_config(str(p)) == {"debug": True}
```

## tests/test_stdlib.py — 14~19

*tests/test_stdlib.py*

```python
from datetime import date, datetime, timedelta, UTC

from solutions import day_range_utc, dedupe

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
```

**💡 테스트를 읽는 것도 학습입니다**

몇몇 테스트는 **정답의 함정을 겨냥**하고 있습니다. `group_by`가 defaultdict를 그대로 반환하면 유령 키 테스트에서, `window`가 버퍼를 그대로 내보내면 스냅샷 테스트에서, `dedupe`가 리스트 `in`을 쓰면 시간 제한에서 걸립니다. 실패 메시지를 먼저 읽고 왜 그런 검사가 있는지 생각해 보세요.

## 자가 채점 루브릭

| 단계 | 기준 |
| --- | --- |
| 1 — 통과 | 테스트가 전부 초록불 |
| 2 — 설명 | 각 함수가 왜 그렇게 구현돼야 하는지 한 문장으로 말할 수 있다 |
| 3 — 타입 | `mypy --strict solutions.py`가 통과한다 |
| 4 — 스타일 | `ruff check solutions.py`가 통과하고, 코어 20파트의 체크리스트를 스스로 돌려 봤다 |
| 5 — 확장 | 테스트를 직접 추가해 자신의 구현에서 빠진 경계 조건을 찾아냈다 |

**💡 다음**

키트를 다 통과했다면 코어는 끝났습니다. 백엔드 트랙(B1–B4)이나 데이터 트랙(D1–D4) 중 지금 하는 일에 가까운 쪽으로 넘어가고, 내부 트랙(22–24)은 성능 문제를 실제로 만났을 때 다시 펼치세요.
