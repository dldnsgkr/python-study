"""B12 · 파일과 모듈 채점."""

import subprocess
import sys
from pathlib import Path

import basics.b12_files as module
from basics.b12_files import (
    append_line,
    count_lines,
    main,
    read_lines,
    word_frequencies,
    write_lines,
)


class TestWriteAndRead:
    def test_roundtrip(self, tmp_path):
        path = str(tmp_path / "out.txt")
        write_lines(path, ["첫 줄", "둘째 줄"])
        assert read_lines(path) == ["첫 줄", "둘째 줄"]

    def test_each_line_ends_with_a_newline(self, tmp_path):
        path = tmp_path / "out.txt"
        write_lines(str(path), ["a", "b"])
        assert path.read_text(encoding="utf-8") == "a\nb\n"

    def test_write_overwrites(self, tmp_path):
        path = str(tmp_path / "out.txt")
        write_lines(path, ["처음"])
        write_lines(path, ["나중"])
        assert read_lines(path) == ["나중"]

    def test_korean_is_written_as_utf8(self, tmp_path):
        path = tmp_path / "ko.txt"
        write_lines(str(path), ["안녕하세요"])
        assert path.read_bytes().decode("utf-8") == "안녕하세요\n"

    def test_empty_list(self, tmp_path):
        path = str(tmp_path / "empty.txt")
        write_lines(path, [])
        assert read_lines(path) == []


class TestAppendLine:
    def test_appends_without_erasing(self, tmp_path):
        path = str(tmp_path / "log.txt")
        write_lines(path, ["첫 줄"])
        append_line(path, "둘째 줄")
        assert read_lines(path) == ["첫 줄", "둘째 줄"]

    def test_creates_the_file_if_missing(self, tmp_path):
        path = str(tmp_path / "new.txt")
        append_line(path, "생성됨")
        assert read_lines(path) == ["생성됨"]


class TestCountLines:
    def test_counts(self, tmp_path):
        path = str(tmp_path / "a.txt")
        write_lines(path, ["a", "b", "c"])
        assert count_lines(path) == 3

    def test_empty_file(self, tmp_path):
        path = tmp_path / "empty.txt"
        path.write_text("", encoding="utf-8")
        assert count_lines(str(path)) == 0


class TestWordFrequencies:
    def test_counts_across_lines(self, tmp_path):
        path = tmp_path / "words.txt"
        path.write_text("apple banana\nApple\n", encoding="utf-8")
        assert word_frequencies(str(path)) == {"apple": 2, "banana": 1}

    def test_empty_file(self, tmp_path):
        path = tmp_path / "empty.txt"
        path.write_text("", encoding="utf-8")
        assert word_frequencies(str(path)) == {}


class TestMainGuard:
    def test_main_returns_a_message(self):
        assert main() == "b12 실행됨"

    def test_the_guard_works_in_both_directions(self, capsys):
        # import 했을 때는 아무 일도 없어야 하고 (이 파일이 이미 import 했다)
        assert capsys.readouterr().out == ""

        # 직접 실행하면 main 이 돌아야 한다
        result = subprocess.run(
            [sys.executable, str(Path(module.__file__))],
            capture_output=True, text=True, check=True,
        )
        assert "b12 실행됨" in result.stdout
