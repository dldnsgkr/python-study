"""확장 03 — 문자열   (docs/12_core_03.md DRILL 03)"""

from __future__ import annotations


def format_row(name: str, amount: float) -> str:
    """이름은 왼쪽 12칸, 금액은 오른쪽 10칸에 천 단위 구분 + 소수점 2자리.

    format_row("coffee", 4500.0) == "coffee         4,500.00"
                                     ^12칸^     ^--10칸--^
    f-문자열의 정렬·너비·서식 지정자를 한 번에 쓰는 연습입니다.
    """
    raise NotImplementedError


def parse_csv_line(line: str) -> list[str | None]:
    """CSV 한 줄을 필드 리스트로. 각 필드는 공백 제거, 빈 필드는 None.

    parse_csv_line(" a , , b ") == ["a", None, "b"]
    parse_csv_line("") == [None]
    """
    raise NotImplementedError


def display_width(s: str) -> int:
    """터미널에서 이 문자열이 차지하는 '칸 수'를 센다.

    display_width("abc") == 3
    display_width("커피") == 4       # 한글은 한 글자가 두 칸

    원본 워크북 03파트가 지적한 문제입니다: f"{name:<12}" 는 글자 **개수**로
    맞추기 때문에 한글이 섞이면 표가 어긋납니다.
    힌트: unicodedata.east_asian_width(ch) 가 "W" 나 "F" 면 두 칸입니다.
    """
    raise NotImplementedError


def pad_display(s: str, width: int) -> str:
    """display_width 기준으로 왼쪽 정렬 패딩. 이미 넘치면 그대로 돌려준다.

    pad_display("커피", 8) 의 display_width 는 8 이어야 합니다.
    이걸 쓰면 한글이 섞인 표도 터미널에서 반듯하게 맞습니다.
    """
    raise NotImplementedError
