"""확장 12 · 데이터 모델링 채점."""

import dataclasses

import pytest

from extra.modeling import OrderLine, from_payload


class TestOrderLine:
    def test_is_a_frozen_dataclass(self):
        assert dataclasses.is_dataclass(OrderLine)
        line = OrderLine(sku="A", qty=2, unit_price=100)
        with pytest.raises(dataclasses.FrozenInstanceError):
            line.qty = 5

    def test_keyword_only(self):
        assert dataclasses.is_dataclass(OrderLine)
        with pytest.raises(TypeError):
            OrderLine("A", 2, 100)

    def test_total(self):
        assert OrderLine(sku="A", qty=3, unit_price=1500).total == 4500

    @pytest.mark.parametrize("qty", [0, -1])
    def test_rejects_non_positive_qty(self, qty):
        with pytest.raises(ValueError):
            OrderLine(sku="A", qty=qty, unit_price=100)

    def test_rejects_negative_price(self):
        with pytest.raises(ValueError):
            OrderLine(sku="A", qty=1, unit_price=-1)

    def test_zero_price_is_allowed(self):
        assert OrderLine(sku="사은품", qty=1, unit_price=0).total == 0

    def test_equality_and_hashability(self):
        a = OrderLine(sku="A", qty=1, unit_price=100)
        b = OrderLine(sku="A", qty=1, unit_price=100)
        assert a == b
        assert len({a, b}) == 1


class TestFromPayload:
    def test_converts(self):
        line = from_payload({"sku": "A", "qty": 2, "unit_price": 100})
        assert line == OrderLine(sku="A", qty=2, unit_price=100)

    def test_missing_key_is_a_value_error_not_key_error(self):
        with pytest.raises(ValueError):
            from_payload({"sku": "A", "qty": 2})

    def test_validation_still_applies(self):
        with pytest.raises(ValueError):
            from_payload({"sku": "A", "qty": 0, "unit_price": 100})
