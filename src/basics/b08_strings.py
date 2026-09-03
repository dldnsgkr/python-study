"""B8 · 문자열 다루기 — 파이썬의 문자열 도구상자

B2에서 문자열이 '값의 한 종류'라는 걸 배웠습니다. 여기서는 실제로 **다루는 법**을 익힙니다.
프로그램이 하는 일의 절반은 문자열을 자르고 붙이고 바꾸는 것입니다.

이번 파트에서 쓰는 도구:
    s.split(구분자)   문자열을 나눠 리스트로       "a,b".split(",")  -> ["a", "b"]
    구분자.join(리스트) 리스트를 이어 문자열로       ",".join(["a","b"]) -> "a,b"
    s.strip()         앞뒤 공백 제거
    s.lower() / .upper()
    s.replace(옛것, 새것)
    s.count(문자)
    s[0]  s[-1]  s[1:4]  s[::-1]     인덱싱과 슬라이싱
"""

from __future__ import annotations


def initials(full_name: str) -> str:
    """이름의 각 단어 첫 글자를 대문자로 이어 붙인다.

    initials("ada lovelace king") == "ALK"
    initials("guido") == "G"

    힌트: split() 으로 단어를 나누고, 각 단어의 [0] 을 모아 join 하세요.
    """
    raise NotImplementedError


def slugify(title: str) -> str:
    """제목을 URL에 쓸 수 있는 형태로 바꾼다.

    slugify("  Hello World  ") == "hello-world"
    slugify("파이썬 완전 정복") == "파이썬-완전-정복"

    앞뒤 공백을 없애고(strip), 소문자로 바꾸고(lower), 공백을 "-" 로 바꾸세요(replace).
    세 가지를 **이어서** 부를 수 있습니다: s.strip().lower().replace(...)
    문자열 메서드는 원본을 바꾸지 않고 **새 문자열을 돌려주기** 때문입니다.
    """
    raise NotImplementedError


def join_with_comma(items: list[str]) -> str:
    """리스트를 ", " 로 이어 붙인다. 빈 리스트면 빈 문자열.

    join_with_comma(["사과", "배", "귤"]) == "사과, 배, 귤"

    ⚠️ for 로 하나씩 더하지 마세요. join 이 훨씬 빠르고 짧습니다.
       "구분자".join(리스트) 처럼 **구분자가 앞에** 온다는 게 처음엔 어색합니다.
    """
    raise NotImplementedError


def mask_email(email: str) -> str:
    """이메일 아이디의 첫 글자만 남기고 나머지를 * 로 가린다.

    mask_email("kim@example.com") == "k**@example.com"
    mask_email("a@b.com") == "a@b.com"        # 한 글자면 가릴 게 없다

    힌트: split("@") 로 나누고, 아이디의 [0] 과 "*" * (길이 - 1) 을 합치세요.
    """
    raise NotImplementedError


def truncate(text: str, limit: int) -> str:
    """길면 잘라 내고 "..." 를 붙인다. 짧으면 그대로.

    truncate("abcdefgh", 5) == "abcde..."
    truncate("abc", 5) == "abc"

    슬라이싱 text[:limit] 을 씁니다. 슬라이싱은 범위를 넘어가도 에러 없이 잘라 냅니다.
    """
    raise NotImplementedError


def title_case(text: str) -> str:
    """각 단어의 첫 글자만 대문자로.

    title_case("hello python world") == "Hello Python World"

    split -> 각 단어 처리 -> join 의 3단 구조를 연습합니다.
    (str.title() 이라는 지름길도 있지만, 이번엔 직접 만들어 보세요)
    """
    raise NotImplementedError


def is_palindrome(text: str) -> bool:
    """앞뒤로 읽어도 같은지 확인한다. 공백과 대소문자는 무시.

    is_palindrome("Never odd or even") is True
    is_palindrome("파이썬") is False

    힌트: 공백을 없애고 소문자로 바꾼 뒤, [::-1] 로 뒤집어 비교하세요.
    [::-1] 은 "처음부터 끝까지 한 칸씩 거꾸로"라는 뜻입니다.
    """
    raise NotImplementedError


def count_char(text: str, char: str) -> int:
    """특정 문자가 몇 번 나오는지 센다. 대소문자 구분 없이.

    count_char("Banana", "a") == 3
    """
    raise NotImplementedError
