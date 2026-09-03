"""B11 · None 과 예외 — 없을 때와 잘못됐을 때

B4의 `grade()` 는 잘못된 점수에 ValueError 를 던졌습니다.
그런데 **그걸 잡는 법**은 아직 안 배웠죠. 여기서 배웁니다.

이번 파트에서 쓰는 도구:
    None                  "값이 없음" 을 나타내는 특별한 값
    if x is None:         None 비교는 == 가 아니라 is 로
    try / except 예외종류:  터질 수 있는 코드를 감싼다
    else:                 예외가 안 났을 때만
    finally:              났든 안 났든 반드시
    raise ValueError(...)  내가 직접 예외를 던진다

자주 만나는 예외:
    ValueError        값이 형식에 안 맞음     int("abc")
    ZeroDivisionError 0으로 나눔
    KeyError          딕셔너리에 없는 키       d["없는키"]
    IndexError        리스트 범위 밖           xs[100]
    TypeError         타입이 안 맞음           1 + "a"
"""

from __future__ import annotations

from typing import Any


def find_user(users: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    """이름이 맞는 첫 사용자를 돌려준다. 없으면 None.

    find_user([{"name": "김"}], "김") == {"name": "김"}
    find_user([], "김") is None

    "없음"을 나타내는 방법은 여러 가지입니다 — 빈 dict, False, 예외, None.
    **찾지 못한 게 정상적인 상황이면 None**, 있어야만 하는데 없으면 예외입니다.
    반환 타입에 `| None` 을 적어 두면 호출한 쪽이 검사를 잊지 않습니다.
    """
    raise NotImplementedError


def display_name(user: dict[str, Any] | None) -> str:
    """사용자의 이름. user 가 None 이면 "손님".

    display_name({"name": "김"}) == "김"
    display_name(None) == "손님"

    ⚠️ None 비교는 `is None` 으로 하세요. `== None` 도 대개 되지만,
       __eq__ 를 이상하게 정의한 객체에서는 틀립니다. is 는 절대 속지 않습니다.
    """
    raise NotImplementedError


def safe_int(text: str, default: int = 0) -> int:
    """문자열을 정수로. 안 되면 default.

    safe_int("42") == 42
    safe_int("숫자아님") == 0
    safe_int("", -1) == -1

    int("abc") 는 ValueError 를 냅니다. try / except ValueError 로 감싸세요.

    ⚠️ `except:` 처럼 벌거벗은 except 는 쓰지 마세요. Ctrl+C 까지 삼켜 버려서
       프로그램을 끌 수 없게 됩니다. 잡을 예외를 **정확히 적으세요.**
    """
    raise NotImplementedError


def safe_divide(a: float, b: float) -> float | None:
    """a / b. b 가 0이면 None.

    safe_divide(10, 2) == 5.0
    safe_divide(1, 0) is None
    """
    raise NotImplementedError


def require_positive(n: int) -> int:
    """양수면 그대로 돌려주고, 아니면 ValueError 를 던진다.

    require_positive(5) == 5
    require_positive(0)  ->  ValueError("0보다 커야 합니다: 0")

    메시지에 **실제 값을 넣으세요.** "잘못된 입력" 보다 "0보다 커야 합니다: -3" 이
    디버깅할 때 100배 낫습니다. f-문자열을 쓰면 됩니다.
    """
    raise NotImplementedError


def parse_scores(raw: list[str]) -> list[int]:
    """숫자로 바꿀 수 있는 것만 골라 정수 리스트로. 나머지는 조용히 건너뛴다.

    parse_scores(["90", "abc", "80"]) == [90, 80]

    한 줄이 깨졌다고 전체를 포기할 수는 없는 상황입니다.
    실무의 로그·CSV 처리가 늘 이렇습니다.
    """
    raise NotImplementedError


def divide_with_log(a: float, b: float, log: list[str]) -> float | None:
    """나눗셈을 하며 어느 갈래를 지났는지 log 에 기록한다.

    성공하면:  log == ["시도", "성공", "정리"]  이고 결과를 반환
    0으로 나누면: log == ["시도", "실패", "정리"]  이고 None 반환

    네 갈래를 다 써 보는 문제입니다:
        try:      "시도" 를 남기고 나눗셈
        except:   "실패"
        else:     예외가 **안 났을 때만** — "성공"
        finally:  났든 안 났든 반드시 — "정리"

    else 가 왜 필요한가: try 블록은 짧을수록 좋습니다. 성공했을 때만 할 일을
    else 로 빼면, 그 코드에서 난 예외를 실수로 잡아 버리는 일이 없습니다.
    """
    raise NotImplementedError
