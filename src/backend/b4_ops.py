"""B4 · 운영 — 설정·로깅·배포   (docs/37_backend_B4.md)

12-factor · 구조화 로깅 · graceful shutdown.
"컨테이너에 넣고 나서" 필요해지는 것들입니다.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextvars import ContextVar

from fastapi import FastAPI

# ── 이건 이미 돼 있습니다 ───────────────────────────────────


def build_logger(name: str, handler: logging.Handler, level: int = logging.INFO) -> logging.Logger:
    """핸들러 하나만 붙은 깨끗한 로거를 만든다(테스트용 배선)."""
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger


# ── DRILL B4-1 · contextvars 기반 trace_id ──────────────────

#: 요청 하나를 따라다니는 추적 ID (배선이라 미리 만들어 뒀습니다).
#: 스레드로컬의 async 버전입니다 — await 로 태스크 경계를 넘어도 같은 값이 따라오고,
#: 자식 태스크가 값을 바꿔도 부모는 오염되지 않습니다(컨텍스트가 복사되니까요).
trace_id_var: ContextVar[str | None] = ContextVar("trace_id", default=None)


def new_trace_id() -> str:
    """새 추적 ID 하나. uuid4 의 hex(32자) 를 쓰세요."""
    raise NotImplementedError


def set_trace_id(value: str) -> None:
    """현재 컨텍스트의 trace_id 를 설정한다."""
    raise NotImplementedError


def get_trace_id() -> str | None:
    """현재 컨텍스트의 trace_id. 설정된 적 없으면 None."""
    raise NotImplementedError


class JsonFormatter(logging.Formatter):
    """로그 한 줄을 JSON 한 줄로 만드는 포매터. `format()` 을 구현하세요.

    반드시 들어갈 키:
        ts      ISO8601 시각 문자열 (self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"))
        level   record.levelname
        logger  record.name
        msg     record.getMessage()          ← record.msg 가 아닙니다. % 포매팅을 적용한 것

    조건부:
        trace_id   get_trace_id() 가 None 이 아닐 때만 (1번)
        exc        record.exc_info 가 있을 때만, self.formatException(record.exc_info)

    그리고 `logger.info("...", extra={"extra_fields": {...}})` 로 넘어온
    dict 를 **최상위에 펼쳐서** 넣으세요.
        payload.update(getattr(record, "extra_fields", {}))

    한글이 \\uXXXX 로 깨지지 않게 json.dumps(..., ensure_ascii=False).

    왜 JSON인가: 로그를 사람이 grep 하는 시대가 아니라, 수집기가 필드로 색인합니다.
    "주문 12345 처리 완료" 를 정규식으로 파싱하는 대신 order_id 필드로 검색하게 됩니다.
    """


# ── DRILL B4-2 · 요청 로깅 미들웨어 ─────────────────────────


def add_timing_middleware(
    app: FastAPI,
    logger: logging.Logger,
    slow_seconds: float = 1.0,
) -> None:
    """요청마다 처리 시간·상태 코드를 남기는 미들웨어를 붙인다.

        @app.middleware("http")
        async def timing(request, call_next): ...

    할 일:
      1. 요청 시작 시 trace_id 를 새로 만들어 set_trace_id 로 설정
      2. 처리 시간 측정 (time.perf_counter)
      3. 로그 한 줄 — extra={"extra_fields": {...}} 로 아래 네 개를 남긴다
             method, path, status, duration_ms   (duration_ms 는 소수 1자리 반올림)
         메시지 본문은 "request" 로 고정하세요(테스트가 필드만 봅니다).
      4. 느린 요청(elapsed > slow_seconds)만 WARNING, 나머지는 INFO
      5. 응답 헤더에 X-Trace-Id 를 실어 보낸다
         — 사용자가 오류를 신고할 때 이 값 하나로 로그를 찾을 수 있습니다

    slow_seconds 를 인자로 받는 이유: 테스트가 1초를 기다리지 않아도 되게 하려고요.
    (09파트의 clock 주입, 17파트의 sleep 주입과 같은 이야기입니다)
    """
    raise NotImplementedError


# ── DRILL B4-3 · graceful shutdown ──────────────────────────


class ShuttingDownError(Exception):
    """종료가 시작된 뒤 들어온 새 요청."""


class GracefulShutdown:
    """SIGTERM 을 받았을 때 "새 요청은 거절, 진행 중인 건 끝까지" 를 관리한다.

    시그널 처리 자체는 테스트하기 어려우니, **정책 부분만** 클래스로 떼어 냈습니다.
    이렇게 떼어 두면 시그널 없이도 로직을 검증할 수 있습니다
    (18파트: 제어할 수 없는 의존성은 경계로 밀어낸다).

    만들 것:
        accepting: bool                 종료 전이면 True (프로퍼티로)
        in_flight: int                  진행 중인 요청 수 (프로퍼티로)

        @asynccontextmanager
        def track_request(self) -> AsyncIterator[None]:
            "요청 하나를 감싼다. 종료 중이면 ShuttingDownError 를 낸다."

        def start_shutdown(self) -> None:
            "이후 track_request 는 거절된다."

        async def wait_idle(self, timeout: float | None = None) -> bool:
            "진행 중인 요청이 0이 될 때까지 기다린다.
             다 끝났으면 True, timeout 안에 못 끝나면 False."

    힌트: asyncio.Event 를 하나 두고, 카운터가 0이 될 때 set() 하세요.
          timeout 은 asyncio.wait_for 로.
          track_request 는 예외가 나도 카운터를 되돌려야 합니다(try/finally).

    ⚠️ 실제 배선(uvicorn lifespan + signal.SIGTERM)은 테스트가 없습니다.
       직접 붙이고 `docker stop` 으로 확인하는 것까지가 원문 과제입니다.
    """

    def __init__(self) -> None:
        raise NotImplementedError
