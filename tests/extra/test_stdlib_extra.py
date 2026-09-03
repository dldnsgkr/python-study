"""확장 16 · 표준 라이브러리 채점."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from extra.stdlib_extra import (
    count_by_extension,
    count_levels,
    dumps_rich,
    loads_rich,
    parse_log_line,
)

LOG_LINES = [
    "[INFO] 2026-01-01T10:00:00 서버 시작",
    "[ERROR] 2026-01-01T10:00:05 DB 연결 실패",
    "형식에 안 맞는 줄",
    "[INFO] 2026-01-01T10:00:07 요청 처리",
    "",
]


class TestCountByExtension:
    def test_counts_and_sizes(self, tmp_path):
        (tmp_path / "a.py").write_text("x" * 10, encoding="utf-8")
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "b.py").write_text("y" * 20, encoding="utf-8")
        (tmp_path / "c.md").write_text("z" * 5, encoding="utf-8")

        result = count_by_extension(tmp_path)
        assert result[".py"] == (2, 30)      # 하위 디렉터리까지 재귀로 센다
        assert result[".md"] == (1, 5)

    def test_extension_is_case_insensitive(self, tmp_path):
        (tmp_path / "a.PY").write_text("x", encoding="utf-8")
        (tmp_path / "b.py").write_text("y", encoding="utf-8")
        assert count_by_extension(tmp_path)[".py"] == (2, 2)

    def test_files_without_extension_use_empty_key(self, tmp_path):
        (tmp_path / "Makefile").write_text("all:", encoding="utf-8")
        assert count_by_extension(tmp_path)[""] == (1, 4)

    def test_directories_are_not_counted(self, tmp_path):
        (tmp_path / "empty_dir").mkdir()
        assert count_by_extension(tmp_path) == {}


class TestParseLogLine:
    def test_named_groups(self):
        assert parse_log_line("[INFO] 2026-01-01T10:00:00 서버 시작") == {
            "level": "INFO",
            "timestamp": "2026-01-01T10:00:00",
            "message": "서버 시작",
        }

    def test_message_may_contain_spaces(self):
        parsed = parse_log_line("[WARN] 2026-01-01T00:00:00 느린 요청 1.5초")
        assert parsed["message"] == "느린 요청 1.5초"

    @pytest.mark.parametrize("line", ["형식 아님", "", "INFO 2026 메시지"])
    def test_bad_lines_return_none(self, line):
        assert parse_log_line(line) is None


class TestCountLevels:
    def test_counts_and_ignores_bad_lines(self):
        assert count_levels(LOG_LINES) == {"INFO": 2, "ERROR": 1}

    def test_returns_plain_dict_without_phantom_keys(self):
        result = count_levels([])
        result.get("DEBUG")
        assert result == {}          # Counter 를 그대로 반환하면 여전히 통과하지만,
        assert type(result) is dict  # 여기서는 평범한 dict 를 요구한다


class TestRichJson:
    def test_roundtrip(self):
        original = {
            "when": datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
            "amount": Decimal("19.99"),
            "name": "커피",
            "qty": 3,
            "tags": ["a", "b"],
        }
        assert loads_rich(dumps_rich(original)) == original

    def test_nested_roundtrip(self):
        original = {"order": {"total": Decimal("100.50"), "items": [{"price": Decimal("1.5")}]}}
        assert loads_rich(dumps_rich(original)) == original

    def test_decimal_precision_survives(self):
        restored = loads_rich(dumps_rich({"x": Decimal("0.1")}))
        assert restored["x"] == Decimal("0.1")
        assert isinstance(restored["x"], Decimal)     # float 로 저장하면 여기서 깨진다

    def test_plain_json_is_untouched(self):
        assert loads_rich(dumps_rich({"a": 1, "b": [1, 2]})) == {"a": 1, "b": [1, 2]}
