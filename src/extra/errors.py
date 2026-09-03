"""확장 13 — 예외   (docs/22_core_13.md DRILL 13)"""

from __future__ import annotations

from collections.abc import Callable, Iterator


def retry_collecting(
    times: int = 3,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable:
    """재시도하되, 전부 실패하면 **모든 시도의 예외**를 ExceptionGroup 으로 묶어 던진다.

    보통의 재시도는 마지막 예외만 남깁니다. 그런데 1번째는 타임아웃,
    2번째는 인증 실패, 3번째는 404 였다면 마지막 것만 봐서는 원인을 못 찾습니다.

    ExceptionGroup("N번 시도 모두 실패", [예외1, 예외2, ...]) 를 던지세요.
    호출하는 쪽은 `except* ValueError:` 로 종류별로 잡을 수 있게 됩니다.
    times 는 총 시도 횟수입니다. 성공하면 그 값을 그대로 돌려줍니다.

    (`exceptions` 가 BaseException 이 아니라 Exception 인 이유: ExceptionGroup 은
     Exception 만 담을 수 있습니다. KeyboardInterrupt 같은 건 BaseExceptionGroup 쪽이고,
     애초에 재시도해서는 안 되는 것들입니다.)
    """
    raise NotImplementedError


def numbers_with_cleanup(log: list[str]) -> Iterator[int]:
    """0, 1, 2 ... 를 무한히 내되, 소비가 끝나면 log 에 "closed" 를 남기는 제너레이터.

    try / finally 로 감싸세요. 소비자가 for 루프 도중 break 해도,
    제너레이터가 close() 되거나 GC 될 때 finally 가 실행됩니다.

    테스트에서 "언제 정리되는가"를 직접 확인하게 됩니다 — 리소스를 쥔
    제너레이터를 만들 때 반드시 알아야 하는 타이밍입니다.
    """
    raise NotImplementedError


def describe_chain(exc: BaseException) -> list[str]:
    """예외 연결 고리를 바깥에서 안쪽으로 훑어 클래스 이름 리스트로 돌려준다.

    describe_chain(ConfigError from FileNotFoundError) == ["ConfigError", "FileNotFoundError"]

    __cause__ (raise ... from exc) 가 있으면 그걸 따라가고,
    없으면 __context__ (except 블록 안에서 그냥 raise) 를 따라갑니다.
    단, __suppress_context__ 가 True 면(= from None) 거기서 멈춥니다.
    """
    raise NotImplementedError
