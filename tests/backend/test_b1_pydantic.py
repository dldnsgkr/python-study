"""B1 · pydantic 채점."""

from dataclasses import FrozenInstanceError, is_dataclass
from decimal import Decimal

import pytest

pytest.importorskip("pydantic", reason="uv sync --group backend 를 먼저 실행하세요")
pytest.importorskip("pydantic_settings", reason="uv sync --group backend 를 먼저 실행하세요")

from pydantic import BaseModel, ValidationError  # noqa: E402

from backend.b1_pydantic import (  # noqa: E402
    AppSettings,
    DomainOrder,
    OrderCreate,
    SignUp,
    describe_errors,
    to_domain,
)

VALID_SIGNUP = {
    "email": "kim@example.com",
    "password": "hunter2024",
    "password_confirm": "hunter2024",
}
VALID_ORDER = {
    "customer_id": 42,
    "lines": [{"sku": "A1", "qty": 2, "unit_price": "1000.00"}],
}


class TestSignUp:
    def test_valid(self):
        assert issubclass(SignUp, BaseModel)
        user = SignUp.model_validate(VALID_SIGNUP)
        assert user.email == "kim@example.com"
        assert user.password == "hunter2024"

    @pytest.mark.parametrize("password,confirm", [
        ("short1", "short1"),           # 8자 미만
        ("onlyletters", "onlyletters"),  # 숫자 없음
        ("12345678", "12345678"),        # 영문 없음
    ])
    def test_weak_password_rejected(self, password, confirm):
        with pytest.raises(ValidationError):
            SignUp.model_validate({**VALID_SIGNUP, "password": password,
                                   "password_confirm": confirm})

    def test_confirm_must_match(self):
        with pytest.raises(ValidationError):
            SignUp.model_validate({**VALID_SIGNUP, "password_confirm": "hunter2025"})

    def test_email_format_is_validated(self):
        with pytest.raises(ValidationError):
            SignUp.model_validate({**VALID_SIGNUP, "email": "not-an-email"})


class TestDescribeErrors:
    def test_nested_location_is_dotted(self):
        with pytest.raises(ValidationError) as info:
            OrderCreate.model_validate({
                "customer_id": 1,
                "lines": [{"sku": "A1", "qty": 0, "unit_price": "10.00"}],
            })
        summary = describe_errors(info.value)
        assert summary[0]["field"] == "lines.0.qty"
        assert "greater_than" in summary[0]["type"]
        assert summary[0]["msg"]

    def test_top_level_field(self):
        with pytest.raises(ValidationError) as info:
            OrderCreate.model_validate({"lines": VALID_ORDER["lines"]})
        assert describe_errors(info.value)[0]["field"] == "customer_id"

    def test_returns_a_list_of_plain_dicts(self):
        with pytest.raises(ValidationError) as info:
            SignUp.model_validate({"email": "x@y.com", "password": "a",
                                   "password_confirm": "a"})
        summary = describe_errors(info.value)
        assert isinstance(summary, list)
        assert set(summary[0]) == {"field", "type", "msg"}


class TestOrderCreate:
    def test_lax_conversion_of_numeric_strings(self):
        order = OrderCreate.model_validate({**VALID_ORDER, "customer_id": "42"})
        assert order.customer_id == 42
        assert isinstance(order.customer_id, int)

    def test_unit_price_is_decimal_not_float(self):
        order = OrderCreate.model_validate(VALID_ORDER)
        assert order.lines[0].unit_price == Decimal("1000.00")
        assert isinstance(order.lines[0].unit_price, Decimal)

    def test_unknown_field_is_rejected(self):
        with pytest.raises(ValidationError):
            OrderCreate.model_validate({**VALID_ORDER, "custmer_id": 42})  # 오타

    def test_whitespace_is_stripped(self):
        order = OrderCreate.model_validate({**VALID_ORDER, "memo": "  급한 주문  "})
        assert order.memo == "급한 주문"

    def test_at_least_one_line(self):
        with pytest.raises(ValidationError):
            OrderCreate.model_validate({"customer_id": 1, "lines": []})

    @pytest.mark.parametrize("qty", [0, -1, 1000])
    def test_qty_bounds(self, qty):
        with pytest.raises(ValidationError):
            OrderCreate.model_validate({
                "customer_id": 1,
                "lines": [{"sku": "A1", "qty": qty, "unit_price": "10.00"}],
            })

    def test_empty_sku_rejected(self):
        with pytest.raises(ValidationError):
            OrderCreate.model_validate({
                "customer_id": 1,
                "lines": [{"sku": "", "qty": 1, "unit_price": "10.00"}],
            })

    def test_html_in_memo_rejected(self):
        with pytest.raises(ValidationError):
            OrderCreate.model_validate({**VALID_ORDER, "memo": "<script>"})

    def test_order_limit(self):
        with pytest.raises(ValidationError):
            OrderCreate.model_validate({
                "customer_id": 1,
                "lines": [{"sku": "A1", "qty": 999, "unit_price": "99999.99"}],
            })

    def test_json_schema_is_generated(self):
        schema = OrderCreate.model_json_schema()
        assert "customer_id" in schema["properties"]      # OpenAPI 문서의 재료


class TestAppSettings:
    def test_missing_required_env_fails_at_construction(self, monkeypatch):
        monkeypatch.delenv("APP_DATABASE_URL", raising=False)
        with pytest.raises(ValidationError):
            AppSettings()                      # 첫 요청이 아니라 부팅에서 터진다

    def test_reads_prefixed_env(self, monkeypatch):
        monkeypatch.setenv("APP_DATABASE_URL", "postgresql://localhost/app")
        settings = AppSettings()
        assert settings.database_url == "postgresql://localhost/app"

    def test_defaults_apply(self, monkeypatch):
        monkeypatch.setenv("APP_DATABASE_URL", "postgresql://localhost/app")
        settings = AppSettings()
        assert settings.redis_url == "redis://localhost:6379/0"
        assert settings.debug is False
        assert settings.max_workers == 4

    def test_bool_and_int_are_parsed_from_strings(self, monkeypatch):
        monkeypatch.setenv("APP_DATABASE_URL", "postgresql://localhost/app")
        monkeypatch.setenv("APP_DEBUG", "true")
        monkeypatch.setenv("APP_MAX_WORKERS", "16")
        settings = AppSettings()
        assert settings.debug is True
        assert settings.max_workers == 16

    def test_invalid_int_is_rejected(self, monkeypatch):
        monkeypatch.setenv("APP_DATABASE_URL", "postgresql://localhost/app")
        monkeypatch.setenv("APP_MAX_WORKERS", "많이")
        with pytest.raises(ValidationError):
            AppSettings()


class TestToDomain:
    def test_converts_to_a_frozen_dataclass(self):
        order = to_domain(OrderCreate.model_validate(VALID_ORDER))
        assert is_dataclass(DomainOrder)
        assert isinstance(order, DomainOrder)
        with pytest.raises(FrozenInstanceError):
            order.customer_id = 1

    def test_carries_the_values_over(self):
        order = to_domain(OrderCreate.model_validate({**VALID_ORDER, "memo": "빠르게"}))
        assert order.customer_id == 42
        assert order.memo == "빠르게"
        assert order.lines[0].sku == "A1"

    def test_lines_are_a_tuple_not_a_list(self):
        order = to_domain(OrderCreate.model_validate(VALID_ORDER))
        assert isinstance(order.lines, tuple)     # 도메인 모델은 통째로 불변이어야 한다
        assert not issubclass(DomainOrder, BaseModel)   # 도메인은 HTTP 를 몰라야 한다

    def test_total(self):
        order = to_domain(OrderCreate.model_validate({
            "customer_id": 1,
            "lines": [
                {"sku": "A", "qty": 2, "unit_price": "1000.00"},
                {"sku": "B", "qty": 3, "unit_price": "500.50"},
            ],
        }))
        assert order.total == Decimal("3501.50")

