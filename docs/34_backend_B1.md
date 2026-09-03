# B1 · pydantic — 타입 힌트를 런타임 계약으로

`BaseModel · validator · Settings`

15파트에서 타입 힌트는 런타임에 아무 일도 하지 않는다고 했습니다. pydantic은 그 힌트를 읽어 **검증·변환·직렬화**를 수행합니다. 백엔드 트랙의 출발점입니다.

*기본*

```python
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

class OrderLine(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    qty: int = Field(gt=0, le=999)
    unit_price: Decimal = Field(ge=0, decimal_places=2)

class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    customer_id: int
    lines: list[OrderLine] = Field(min_length=1)
    memo: str | None = None
    requested_at: datetime | None = None

    @field_validator("memo")
    @classmethod
    def no_html(cls, v: str | None) -> str | None:
        if v and "<" in v:
            raise ValueError("HTML 태그는 사용할 수 없습니다")
        return v

    @model_validator(mode="after")
    def check_total(self):
        if sum(l.qty * l.unit_price for l in self.lines) > 10_000_000:
            raise ValueError("단일 주문 한도를 초과했습니다")
        return self
```

*사용*

```python
data = {"customer_id": "42", "lines": [{"sku": "A1", "qty": "2", "unit_price": "1000.00"}]}

order = OrderCreate.model_validate(data)     # 문자열 "42" → int 42 로 강제 변환
order.customer_id                            # 42 (int)

order.model_dump()                           # dict
order.model_dump_json()                      # JSON 문자열
OrderCreate.model_json_schema()              # JSON Schema — OpenAPI 문서의 재료
```

**⚠️ Gotcha**

기본 모드는 **관대한 변환(lax)**입니다. `"42"`가 `42`가 되고 `1`이 `True`가 됩니다. 외부 입력을 엄격히 다뤄야 하면 `model_config = ConfigDict(strict=True)`를 켜세요. 또 `extra="forbid"`를 안 걸면 오타 난 필드가 **조용히 무시**됩니다 — API 계약에서는 거의 항상 켜야 합니다.

*설정 관리*

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")

    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    debug: bool = False
    max_workers: int = 4

settings = Settings()      # 환경변수 APP_DATABASE_URL 등을 읽어 검증까지 완료
```

**☕ JVM 개발자 노트**

`BaseModel` ≈ `@Valid`가 붙은 DTO + Jackson. `BaseSettings` ≈ `@ConfigurationProperties`. 차이는 **애플리케이션 시작 시점에 설정이 검증된다**는 점입니다. 잘못된 환경변수는 첫 요청이 아니라 부팅에서 즉시 실패합니다 — fail fast가 기본값입니다.

**💡 경계 모델과 도메인 모델을 분리하세요**

HTTP 요청/응답용 pydantic 모델과, 비즈니스 로직용 `dataclass`(12파트)를 나누면 API 스펙 변경이 도메인으로 새지 않습니다. 경계에서 `OrderCreate → Order` 변환 함수를 하나 두는 것이 실무에서 오래 버티는 구조입니다.

### 🏋 DRILL B1 — pydantic

1. 회원가입 요청 모델을 만드세요. 이메일 형식, 비밀번호 8자 이상·영문/숫자 포함, 비밀번호 확인 일치를 `model_validator`로 검증합니다.
2. 잘못된 입력을 넣고 `ValidationError.errors()` 구조를 출력해 `loc`/`type`/`msg`가 어떻게 구성되는지 정리하세요.
3. 같은 도메인을 `dataclass`와 `BaseModel`로 각각 만들고 100만 건 생성 속도와 메모리를 비교하세요.
4. `Settings`에 필수 환경변수를 하나 두고, 값이 없을 때 부팅이 즉시 실패하는지 확인하세요.

---

**🟢 1번 예시 답**

```python
import re
from pydantic import BaseModel, EmailStr, model_validator

class SignUp(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def validate_password(self):
        if len(self.password) < 8:
            raise ValueError("비밀번호는 8자 이상이어야 합니다")
        if not (re.search(r"[A-Za-z]", self.password) and re.search(r"\d", self.password)):
            raise ValueError("영문과 숫자를 모두 포함해야 합니다")
        if self.password != self.password_confirm:
            raise ValueError("비밀번호가 일치하지 않습니다")
        return self
```

---
