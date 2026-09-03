"""확장 15 · 타입 채점 (런타임 동작만. 진짜 채점은 `uv run mypy` 입니다)."""

from extra.typed import get


def test_returns_value_when_present():
    assert get("a") == "1"


def test_returns_none_without_default():
    assert get("없는키") is None


def test_returns_default_when_given():
    assert get("없는키", "기본값") == "기본값"
