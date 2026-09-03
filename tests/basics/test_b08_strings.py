"""B8 · 문자열 다루기 채점."""

import pytest

from basics.b08_strings import (
    count_char,
    initials,
    is_palindrome,
    join_with_comma,
    mask_email,
    slugify,
    title_case,
    truncate,
)


class TestInitials:
    def test_multiple_words(self):
        assert initials("ada lovelace king") == "ALK"

    def test_single_word(self):
        assert initials("guido") == "G"

    def test_already_uppercase(self):
        assert initials("Grace Hopper") == "GH"


class TestSlugify:
    def test_trims_lowers_and_hyphenates(self):
        assert slugify("  Hello World  ") == "hello-world"

    def test_korean(self):
        assert slugify("파이썬 완전 정복") == "파이썬-완전-정복"

    def test_does_not_mutate_the_original(self):
        title = "  Hello  "
        slugify(title)
        assert title == "  Hello  "      # 문자열은 불변이라 원래 바뀔 수 없다


class TestJoinWithComma:
    def test_joins(self):
        assert join_with_comma(["사과", "배", "귤"]) == "사과, 배, 귤"

    def test_single(self):
        assert join_with_comma(["사과"]) == "사과"

    def test_empty(self):
        assert join_with_comma([]) == ""      # 뒤에 쉼표가 남으면 실패한다


class TestMaskEmail:
    def test_masks_the_local_part(self):
        assert mask_email("kim@example.com") == "k**@example.com"

    def test_single_letter_local_part(self):
        assert mask_email("a@b.com") == "a@b.com"

    def test_long_local_part(self):
        assert mask_email("developer@corp.io") == "d********@corp.io"


class TestTruncate:
    def test_cuts_and_adds_ellipsis(self):
        assert truncate("abcdefgh", 5) == "abcde..."

    def test_short_text_is_untouched(self):
        assert truncate("abc", 5) == "abc"

    def test_exact_length_is_untouched(self):
        assert truncate("abcde", 5) == "abcde"


class TestTitleCase:
    def test_capitalizes_each_word(self):
        assert title_case("hello python world") == "Hello Python World"

    def test_single_word(self):
        assert title_case("python") == "Python"

    def test_keeps_inner_letters(self):
        assert title_case("mcDonald farm") == "McDonald Farm"


class TestIsPalindrome:
    @pytest.mark.parametrize("text,expected", [
        ("Never odd or even", True),
        ("racecar", True),
        ("파이썬", False),
        ("", True),
        ("기러기", True),
    ])
    def test_palindrome(self, text, expected):
        assert is_palindrome(text) is expected


class TestCountChar:
    def test_ignores_case(self):
        assert count_char("Banana", "a") == 3

    def test_not_found(self):
        assert count_char("abc", "z") == 0
