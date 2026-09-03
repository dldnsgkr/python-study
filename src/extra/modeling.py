"""확장 12 — 데이터 모델링   (docs/21_core_12.md DRILL 12)"""

from __future__ import annotations

from typing import TypedDict


class OrderLine:
    """주문 한 줄. **frozen dataclass** 로 만드세요 (지금은 빈 클래스입니다).

        @dataclass(frozen=True, kw_only=True)
        class OrderLine:
            sku: str
            qty: int
            unit_price: int

    - __post_init__ 에서 검증: qty > 0 아니면 ValueError, unit_price >= 0 아니면 ValueError
    - total 프로퍼티: qty * unit_price
    - frozen 이므로 line.qty = 5 는 실패해야 합니다
    - 같은 값이면 == 이고 set 에 넣을 수 있어야 합니다 (frozen dataclass 가 공짜로 줍니다)
    - kw_only 이므로 OrderLine("A", 1, 100) 처럼 위치 인자로는 못 만듭니다
    """


class OrderPayload(TypedDict):
    """외부 JSON 응답의 모양. dict 지만 키와 타입이 정해져 있다고 선언한 것."""

    sku: str
    qty: int
    unit_price: int


def from_payload(payload: OrderPayload) -> OrderLine:
    """외부에서 들어온 dict 를 내부 도메인 객체로 바꾸는 어댑터.

    빠진 키가 있으면 KeyError 대신 ValueError("필수 키 누락: xxx") 를 내세요.
    외부 스키마와 내부 모델 사이에 이런 변환 지점을 하나 두면,
    바깥이 바뀌어도 고칠 곳이 한 군데뿐입니다.
    """
    raise NotImplementedError
