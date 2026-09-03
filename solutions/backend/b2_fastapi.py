"""B2 모범답안."""

from __future__ import annotations

import time
from dataclasses import dataclass, replace
from typing import Annotated

from fastapi import Depends, FastAPI, Path, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


@dataclass(frozen=True)
class OrderRecord:
    id: int
    customer_id: int
    memo: str | None = None


class OrderRepo:
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


class DomainError(Exception):
    code = "domain_error"
    status = 400


class NotFoundError(DomainError):
    code = "not_found"
    status = 404


class ConflictError(DomainError):
    code = "conflict"
    status = 409


class OrderIn(BaseModel):
    customer_id: int
    memo: str | None = None


class OrderPatch(BaseModel):
    memo: str | None = None


class OrderOut(BaseModel):
    id: int
    customer_id: int
    memo: str | None = None


class OrderPage(BaseModel):
    items: list[OrderOut]
    next_cursor: int | None = None


def get_repo() -> OrderRepo:
    raise RuntimeError("주입되지 않았습니다")


RepoDep = Annotated[OrderRepo, Depends(get_repo)]


def create_app(repo: OrderRepo) -> FastAPI:
    app = FastAPI(title="Order API", version="1.0.0")
    app.dependency_overrides[get_repo] = lambda: repo

    @app.exception_handler(DomainError)
    async def handle_domain_error(request, exc: DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status,
            content={"code": exc.code, "message": str(exc)},
        )

    def _require(order: OrderRecord | None) -> OrderRecord:
        if order is None:
            raise NotFoundError("주문을 찾을 수 없습니다")
        return order

    @app.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
    async def create_order(payload: OrderIn, orders: RepoDep) -> OrderRecord:
        return orders.create(payload.customer_id, payload.memo)

    @app.get("/orders", response_model=OrderPage)
    async def list_orders(
        orders: RepoDep,
        cursor: Annotated[int | None, Query(ge=1)] = None,
        limit: Annotated[int, Query(ge=1, le=100)] = 10,
    ) -> OrderPage:
        rows = orders.page(cursor, limit)
        next_cursor = rows[-1].id if len(rows) == limit else None
        return OrderPage(
            items=[OrderOut.model_validate(r, from_attributes=True) for r in rows],
            next_cursor=next_cursor,
        )

    @app.get("/orders/{order_id}", response_model=OrderOut)
    async def get_order(orders: RepoDep, order_id: Annotated[int, Path(gt=0)]) -> OrderRecord:
        return _require(orders.get(order_id))

    @app.patch("/orders/{order_id}", response_model=OrderOut)
    async def patch_order(
        orders: RepoDep,
        payload: OrderPatch,
        order_id: Annotated[int, Path(gt=0)],
    ) -> OrderRecord:
        _require(orders.get(order_id))
        return _require(orders.update(order_id, payload.memo))

    @app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_order(orders: RepoDep, order_id: Annotated[int, Path(gt=0)]) -> None:
        if not orders.delete(order_id):
            raise NotFoundError("주문을 찾을 수 없습니다")

    return app


SLEEP_SECONDS = 0.1


def create_blocking_app(sleep_seconds: float = SLEEP_SECONDS) -> FastAPI:
    app = FastAPI()

    @app.get("/report")
    def report() -> dict[str, bool]:      # async def 가 아니라 def — 스레드풀로 간다
        time.sleep(sleep_seconds)
        return {"ok": True}

    return app
