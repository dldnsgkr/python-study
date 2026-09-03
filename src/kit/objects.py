"""코어 01~05 — 객체 모델 · 숫자 · 문자열 · 시퀀스 · 매핑과 집합

docs/10_core_01.md ~ docs/14_core_05.md
"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable
from decimal import Decimal
from typing import Any


# ── 01 객체 모델 ────────────────────────────────────────────
def with_key(d: dict, path: list[str], value: Any) -> dict:
    """원본을 변경하지 않고 path 위치의 값을 바꾼 새 dict를 반환한다.

    with_key({"user": {"name": "kim"}}, ["user", "name"], "lee")
        -> {"user": {"name": "lee"}}   (원본의 "kim" 은 그대로)

    중간 키가 없으면 만들어 줍니다: with_key({}, ["a", "b"], 1) -> {"a": {"b": 1}}
    함정: 얕은 복사만 하면 중첩 dict를 원본과 공유해 원본까지 오염됩니다.
    """
    raise NotImplementedError


# ── 02 숫자 ────────────────────────────────────────────────
def total_with_vat(unit_price: str, qty: int) -> Decimal:
    """부가세 10%를 더한 총액을 1원 단위로 반올림(HALF_UP)해 반환한다.

    입력은 **문자열**입니다. float 로 바꾸는 순간 돈 계산이 틀어집니다.
    반환 타입도 Decimal 이어야 합니다.
    """
    raise NotImplementedError


# ── 03 문자열 ──────────────────────────────────────────────
def split_once(s: str, sep: str = "=") -> tuple[str, str]:
    """첫 구분자 기준으로만 두 조각으로 나눈다. 구분자가 없으면 (s, "").

    "key=value=extra" -> ("key", "value=extra")
    partition 과 split(sep, 1) 두 가지로 각각 짜 보고 차이를 확인하세요.
    """
    raise NotImplementedError


# ── 04 시퀀스 ──────────────────────────────────────────────
def rotate(xs: list, k: int) -> list:
    """오른쪽으로 k칸 회전한 새 리스트. k가 길이보다 커도 동작한다.

    rotate([1,2,3,4,5], 2) == [4,5,1,2,3]
    함정: k == 0 일 때 xs[-0:] 는 xs[0:] 라 전체가 됩니다. 분기가 필요합니다.
    """
    raise NotImplementedError


def flatten(xs: Iterable) -> list:
    """임의 깊이의 list/tuple을 평탄화한다. 문자열은 펼치지 않는다.

    flatten([1, [2, [3, [4]]], (5, 6)]) == [1, 2, 3, 4, 5, 6]
    flatten(["ab", ["cd"]]) == ["ab", "cd"]        # 문자열은 그대로
    """
    raise NotImplementedError


# ── 05 매핑과 집합 ─────────────────────────────────────────
def group_by(records: Iterable[Any], key: Callable[[Any], Hashable]) -> dict:
    """key(record) 값으로 묶어 {키: [레코드, ...]} 를 반환한다.

    함정: defaultdict 를 그대로 반환하면 나중에 없는 키를 조회한 것만으로
    빈 리스트가 생겨 버립니다(유령 키). 반환 전에 평범한 dict 로 바꾸세요.
    """
    raise NotImplementedError


def diff(old: dict, new: dict) -> dict:
    """두 dict의 차이를 집합 연산으로 계산한다.

    {"added": {...}, "removed": {...}, "changed": {키: (이전, 이후)}}
    """
    raise NotImplementedError
