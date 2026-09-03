"""코어 10~13 채점."""

import json

import pytest

from kit.oop import ConfigError, Money, Status, Temperature, load_config, transition


class TestTemperature:
    def test_conversion_both_ways(self):
        t = Temperature(100)
        assert t.fahrenheit == pytest.approx(212)
        t.fahrenheit = 32
        assert t.celsius == pytest.approx(0)

    def test_fahrenheit_is_a_property_not_a_stored_field(self):
        assert isinstance(type(Temperature()).__dict__["fahrenheit"], property)

    def test_fahrenheit_follows_celsius_changes(self):
        t = Temperature(0)
        t.celsius = 100
        assert t.fahrenheit == pytest.approx(212)   # __init__ 에서 계산해 두면 실패한다


class TestMoney:
    def test_add_same_currency(self):
        assert (Money(1000) + Money(500)).amount == 1500

    def test_subtract_same_currency(self):
        assert (Money(1000) - Money(300)).amount == 700

    def test_reject_different_currency(self):
        with pytest.raises(TypeError):
            Money(1000, "KRW") + Money(10, "USD")
        with pytest.raises(TypeError):
            Money(1000, "KRW") - Money(10, "USD")
        with pytest.raises(TypeError):
            Money(1000, "KRW") < Money(10, "USD")

    def test_comparison_and_sorting(self):
        xs = sorted([Money(300), Money(100), Money(200)])
        assert [m.amount for m in xs] == [100, 200, 300]

    def test_sum_works(self):
        assert sum([Money(100), Money(200)]).amount == 300

    def test_equality_and_hash(self):
        assert Money(100) == Money(100)
        assert len({Money(100), Money(100), Money(200)}) == 2

    def test_different_currency_is_not_equal(self):
        assert Money(100, "KRW") != Money(100, "USD")

    def test_repr_is_informative(self):
        assert "100" in repr(Money(100))


class TestTransition:
    @pytest.mark.parametrize("cur,nxt", [
        (Status.PENDING, Status.PAID),
        (Status.PENDING, Status.CANCELED),
        (Status.PAID, Status.CANCELED),
    ])
    def test_allowed(self, cur, nxt):
        assert transition(cur, nxt) is nxt

    @pytest.mark.parametrize("cur,nxt", [
        (Status.PAID, Status.PENDING),
        (Status.CANCELED, Status.PAID),
        (Status.CANCELED, Status.PENDING),
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

    def test_broken_json_also_becomes_config_error(self, tmp_path):
        p = tmp_path / "broken.json"
        p.write_text("{not json", encoding="utf-8")
        with pytest.raises(ConfigError) as info:
            load_config(str(p))
        assert isinstance(info.value.__cause__, json.JSONDecodeError)
