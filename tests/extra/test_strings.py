"""확장 03 · 문자열 채점."""

import pytest

from extra.strings import display_width, format_row, pad_display, parse_csv_line


class TestFormatRow:
    def test_layout(self):
        assert format_row("coffee", 4500.0) == "coffee" + " " * 8 + "4,500.00"

    def test_total_width_is_22(self):
        assert len(format_row("a", 1.0)) == 22

    def test_thousands_and_two_decimals(self):
        assert format_row("x", 1234567.5).endswith("1,234,567.50")


class TestParseCsvLine:
    def test_strips_and_nulls_empty(self):
        assert parse_csv_line(" a , , b ") == ["a", None, "b"]

    def test_empty_line(self):
        assert parse_csv_line("") == [None]

    def test_keeps_inner_spaces(self):
        assert parse_csv_line(" hello world , x") == ["hello world", "x"]


class TestDisplayWidth:
    @pytest.mark.parametrize("text,width", [
        ("abc", 3), ("커피", 4), ("", 0), ("커피 A", 6), ("가나다라", 8),
    ])
    def test_width(self, text, width):
        assert display_width(text) == width


class TestPadDisplay:
    def test_korean_pads_to_visual_width(self):
        assert display_width(pad_display("커피", 8)) == 8
        assert pad_display("커피", 8) == "커피    "

    def test_ascii(self):
        assert pad_display("ab", 5) == "ab   "

    def test_already_too_long_is_untouched(self):
        assert pad_display("가나다", 2) == "가나다"

    def test_table_lines_up(self):
        rows = [("커피", 4500), ("sandwich", 8900), ("아메리카노", 4000)]
        widths = {display_width(pad_display(name, 14)) for name, _ in rows}
        assert widths == {14}     # 한 줄이라도 어긋나면 집합 크기가 커진다
