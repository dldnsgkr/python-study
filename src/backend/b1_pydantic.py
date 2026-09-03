"""B1 · pydantic — 타입 힌트를 런타임 계약으로   (docs/34_backend_B1.md)

15파트에서 타입 힌트는 런타임에 아무 일도 하지 않는다고 했습니다.
pydantic은 그 힌트를 읽어 검증·변환·직렬화를 합니다.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from pydantic import BaseModel, ValidationError

# ── DRILL B1-1 · 회원가입 요청 모델 ─────────────────────────


class SignUp(BaseModel):
    """회원가입 요청.

    필드: email(EmailStr), password(str), password_confirm(str)

    `@model_validator(mode="after")` 로 검증하세요:
      - 비밀번호 8자 이상          아니면 ValueError("비밀번호는 8자 이상이어야 합니다")
      - 영문과 숫자를 모두 포함     아니면 ValueError("영문과 숫자를 모두 포함해야 합니다")
      - password == password_confirm  아니면 ValueError("비밀번호가 일치하지 않습니다")

    mode="after" 인 이유: 개별 필드 검증이 끝난 뒤 **모델 전체**를 보기 때문입니다.
    두 필드를 비교하는 검증은 mode="before" 로는 깔끔히 쓸 수 없습니다.
    """


# ── DRILL B1-2 · ValidationError 구조 읽기 ──────────────────


def describe_errors(exc: ValidationError) -> list[dict[str, str]]:
    """ValidationError 를 사람이 읽을 수 있는 요약으로 바꾼다.

    [{"field": "lines.0.qty", "type": "greater_than", "msg": "..."}, ...]

    - field: errors()[i]["loc"] 튜플을 "." 로 이어 붙인 것. 중첩 리스트 인덱스는 숫자 그대로.
      loc 가 비어 있으면(모델 전체 오류) "__root__".
    - type, msg: errors() 의 같은 이름 값을 그대로.

    API가 400을 돌려줄 때 클라이언트에게 "어느 필드가 왜 틀렸는지" 알려주는 부분입니다.
    pydantic 의 loc 튜플을 그대로 노출하면 프런트가 파싱하기 어렵습니다.
    """
    raise NotImplementedError


# ── DRILL B1-1' · 경계 모델 (extra="forbid" 의 중요성) ──────


class OrderLineIn(BaseModel):
    """주문 한 줄의 **입력** 모델.

    sku:        str,     1~64자
    qty:        int,     0 초과 999 이하
    unit_price: Decimal, 0 이상, 소수점 2자리까지

    Field(min_length=..., gt=..., le=..., ge=..., decimal_places=...) 를 쓰세요.
    """


class OrderCreate(BaseModel):
    """주문 생성 요청.

    model_config 로 두 가지를 켜세요:
      extra="forbid"            — 모르는 필드가 오면 거부.
                                  안 켜면 오타 난 필드가 **조용히 무시**됩니다.
      str_strip_whitespace=True — 문자열 앞뒤 공백 자동 제거

    필드:
      customer_id: int
      lines: list[OrderLineIn]   최소 1개 (Field(min_length=1))
      memo: str | None = None
      
    검증:
      - @field_validator("memo"): "<" 가 들어 있으면 ValueError("HTML 태그는 사용할 수 없습니다")
      - @model_validator(mode="after"): 총액(qty * unit_price 합)이 10_000_000 초과면
        ValueError("단일 주문 한도를 초과했습니다")
    """


# ── DRILL B1-4 · 설정은 부팅에서 검증된다 ───────────────────


class AppSettings:
    """환경변수 기반 설정. **BaseSettings 를 상속하도록 바꾸세요.**

        class AppSettings(BaseSettings):
            model_config = SettingsConfigDict(env_prefix="APP_")
            ...

    필드:
      database_url: str            (기본값 없음 — 필수)
      redis_url: str = "redis://localhost:6379/0"
      debug: bool = False
      max_workers: int = 4

    APP_DATABASE_URL 이 없으면 **객체를 만드는 순간** ValidationError 가 나야 합니다.
    첫 요청이 아니라 부팅에서 실패하는 것 — 그게 fail fast 입니다.

    (env_file 은 일부러 쓰지 않습니다. 테스트가 실행 디렉터리의 .env 에 영향을 받으면
     "왜 로컬에서만 통과하지" 같은 문제가 생깁니다.)
    """


# ── 💡 경계 모델과 도메인 모델을 분리하기 ───────────────────


@dataclass(frozen=True)
class DomainLine:
    sku: str
    qty: int
    unit_price: Decimal


@dataclass(frozen=True)
class DomainOrder:
    """비즈니스 로직이 쓰는 모델. HTTP 를 모릅니다.

    **frozen dataclass 로 만드세요** (지금은 필드가 이미 선언돼 있습니다).
    `total` 프로퍼티는 직접 추가하세요 — 모든 줄의 qty * unit_price 합(Decimal).
    """

    customer_id: int
    lines: tuple[DomainLine, ...]
    memo: str | None = None


def to_domain(payload: OrderCreate) -> DomainOrder:
    """경계 모델(pydantic) → 도메인 모델(dataclass) 변환.

    이 함수 하나를 경계에 두면 API 스펙이 바뀌어도 도메인 코드는 그대로입니다.
    swim_back 의 crawler/schema.py 가 하는 일과 정확히 같은 역할입니다.
    """
    raise NotImplementedError
