"""B2 · FastAPI — 타입이 곧 API 스펙   (docs/35_backend_B2.md)

경로 파싱, 쿼리 기본값, 본문 검증, 응답 직렬화, OpenAPI 문서까지
**전부 함수 시그니처에서 나옵니다.**
"""

from __future__ import annotations

import time
from dataclasses import dataclass, replace

from fastapi import FastAPI

# ── 이건 이미 돼 있습니다 — 저장소(리포지터리) ──────────────
# B2 의 주제는 HTTP 계층이라 저장소는 인메모리로 제공합니다.
# 진짜 DB 버전은 B3 에서 만듭니다.


@dataclass(frozen=True)
class OrderRecord:
    id: int
    customer_id: int
    memo: str | None = None


class OrderRepo:
    """id 오름차순으로 정렬된 인메모리 주문 저장소."""

    def __init__(self) -> None:
        self._rows: dict[int, OrderRecord] = {}
        self._next_id = 1

    def create(self, customer_id: int, memo: str | None = None) -> OrderRecord:
        record = OrderRecord(id=self._next_id, customer_id=customer_id, memo=memo)
        self._rows[record.id] = record
        self._next_id += 1
        return record

    def get(self, order_id: int) -> OrderRecord | None:
        return self._rows.get(order_id)

    def page(self, cursor: int | None, limit: int) -> list[OrderRecord]:
        """id > cursor 인 것부터 오름차순으로 limit 개."""
        after = cursor or 0
        rows = [r for r in sorted(self._rows.values(), key=lambda r: r.id) if r.id > after]
        return rows[:limit]

    def update(self, order_id: int, memo: str | None) -> OrderRecord | None:
        record = self._rows.get(order_id)
        if record is None:
            return None
        updated = replace(record, memo=memo)
        self._rows[order_id] = updated
        return updated

    def delete(self, order_id: int) -> bool:
        return self._rows.pop(order_id, None) is not None


# ── DRILL B2-2 · 도메인 예외 계층 ───────────────────────────


class DomainError(Exception):
    """모든 도메인 예외의 뿌리. **여기부터 직접 만드세요.**

    클래스 속성 두 개를 갖습니다:
        code: str    응답 본문에 나갈 기계용 코드
        status: int  매핑될 HTTP 상태 코드

    DomainError 자체는 code="domain_error", status=400.

    아래 두 개를 상속으로 만드세요:
        NotFoundError  code="not_found", status=404
        ConflictError  code="conflict",  status=409

    13파트의 "루트 예외 하나" 패턴입니다. 핸들러 하나로 전부 잡을 수 있고,
    나중에 예외를 추가해도 HTTP 계층은 손대지 않습니다.
    """


class NotFoundError(DomainError):
    """code="not_found", status=404 를 붙이세요."""


class ConflictError(DomainError):
    """code="conflict", status=409 를 붙이세요."""


# ── DRILL B2-1 · 3 · CRUD 와 커서 페이지네이션 ──────────────


def create_app(repo: OrderRepo) -> FastAPI:
    """주문 API 앱을 만들어 돌려준다.

    ## 만들 엔드포인트

    | 메서드 | 경로 | 성공 | 본문/파라미터 |
    | --- | --- | --- | --- |
    | POST   | /orders             | 201 | {"customer_id": int, "memo": str\\|null} |
    | GET    | /orders/{order_id}  | 200 | order_id 는 0보다 커야 함 |
    | GET    | /orders             | 200 | ?cursor=&limit= |
    | PATCH  | /orders/{order_id}  | 200 | {"memo": str\\|null} |
    | DELETE | /orders/{order_id}  | 204 | 본문 없음 |

    응답 모델 OrderOut = {"id": int, "customer_id": int, "memo": str|null}

    ## 커서 페이지네이션 (3번)

    GET /orders?cursor=<마지막으로 본 id>&limit=<개수>
      - limit 기본 10, 1 이상 100 이하  → Query(default=10, ge=1, le=100)
      - 응답 {"items": [OrderOut, ...], "next_cursor": int | null}
      - next_cursor 는 **꽉 찬 페이지일 때만** 마지막 항목의 id, 아니면 null
        (다음 페이지가 있는지를 알려주는 값입니다. 마지막 페이지에서 null 이 나와야
         클라이언트가 "여기서 끝"을 압니다)
      - offset 이 아니라 커서를 쓰는 이유: 중간에 행이 추가/삭제돼도 항목이
        건너뛰거나 중복되지 않습니다.

    ## 없는 주문 (2번)

    저장소가 None 을 주면 `NotFoundError("주문을 찾을 수 없습니다")` 를 던지세요.
    HTTPException 을 직접 쓰지 마세요 — 도메인 예외를 던지고, 아래 핸들러가 변환합니다.

    ## 예외 핸들러 (2번)

    `@app.exception_handler(DomainError)` 하나로 전부 처리:
        JSONResponse(status_code=exc.status, content={"code": exc.code, "message": str(exc)})

    ## 저장소 주입

    Depends 로 받으세요. 시그니처가 곧 의존성 그래프입니다:

        def get_repo() -> OrderRepo:
            raise RuntimeError("주입되지 않았습니다")     # 실제 구현은 아래에서 덮어씀

        RepoDep = Annotated[OrderRepo, Depends(get_repo)]

        app.dependency_overrides[get_repo] = lambda: repo

    테스트가 `dependency_overrides` 로 가짜 저장소를 끼워 넣을 수 있어야 합니다.
    몽키패치보다 훨씬 안정적입니다 — 의존성 그래프의 노드만 갈아 끼우니까요.
    """
    raise NotImplementedError


# ── DRILL B2-4 · async 안에서 블로킹하면 생기는 일 ──────────

SLEEP_SECONDS = 0.1


def create_blocking_app(sleep_seconds: float = SLEEP_SECONDS) -> FastAPI:
    """`GET /report` 하나만 있는 앱. 핸들러는 time.sleep(sleep_seconds) 를 호출한다.

    ⚠️ 이 문제의 전부는 **핸들러를 `def` 로 쓸지 `async def` 로 쓸지**입니다.

    `async def` + `time.sleep()` 을 쓰면 이벤트 루프가 통째로 멈춰서 요청 5개가
    순차 처리됩니다(0.5초). 그냥 `def` 로 선언하면 FastAPI 가 스레드풀에서
    돌려 주어 동시에 처리됩니다(0.1초대).

    동기 라이브러리(동기 DB 드라이버, requests 등)를 써야 할 때 기억해야 하는
    규칙입니다. 최악의 조합은 `async def` + 동기 블로킹입니다.

    테스트는 동시 요청 5개의 총 소요 시간을 잽니다.
    """
    raise NotImplementedError
