"""B3 모범답안."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from sqlalchemy import ForeignKey, Select, String, event, func, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)


class Base(DeclarativeBase):
    pass


def make_engine(url: str = "sqlite+aiosqlite:///:memory:", echo: bool = False) -> AsyncEngine:
    return create_async_engine(url, echo=echo)


def make_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


async def setup_schema(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@contextmanager
def count_queries(engine: AsyncEngine) -> Iterator[list[str]]:
    statements: list[str] = []

    def before(conn, cursor, statement, parameters, context, executemany):  # noqa: ANN001
        statements.append(statement)

    event.listen(engine.sync_engine, "before_cursor_execute", before)
    try:
        yield statements
    finally:
        event.remove(engine.sync_engine, "before_cursor_execute", before)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    stock: Mapped[int]


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    lines: Mapped[list[OrderLine]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="raise",              # 실수로 지연 로딩하면 조용히 느려지는 대신 터진다
    )


class OrderLine(Base):
    __tablename__ = "order_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    sku: Mapped[str] = mapped_column(String(64))
    qty: Mapped[int]

    order: Mapped[Order] = relationship(back_populates="lines")


async def orders_with_lines(session: AsyncSession, customer_id: int) -> list[Order]:
    stmt = (
        select(Order)
        .where(Order.customer_id == customer_id)
        .options(selectinload(Order.lines))    # 주문 1번 + 라인 IN 1번 = 총 2번
        .order_by(Order.id.desc())
    )
    return list((await session.scalars(stmt)).all())


async def order_counts_by_customer(
    session: AsyncSession, min_orders: int
) -> list[tuple[int, int]]:
    count = func.count(Order.id).label("cnt")
    stmt = (
        select(Order.customer_id, count)
        .group_by(Order.customer_id)
        .having(count >= min_orders)
        .order_by(count.desc(), Order.customer_id.asc())
    )
    return [(row[0], row[1]) for row in (await session.execute(stmt)).all()]


class OutOfStockError(Exception):
    """재고가 모자랄 때."""


class ProductNotFoundError(Exception):
    """상품이 없을 때."""


def stock_lock_stmt(product_id: int) -> Select[tuple[Product]]:
    return select(Product).where(Product.id == product_id).with_for_update()


async def decrement_stock(session: AsyncSession, product_id: int, qty: int) -> int:
    product = (await session.scalars(stock_lock_stmt(product_id))).one_or_none()
    if product is None:
        raise ProductNotFoundError(f"상품 {product_id} 없음")
    if product.stock < qty:
        raise OutOfStockError(f"재고 부족: {product.stock} < {qty}")
    product.stock -= qty
    await session.flush()
    return product.stock


@dataclass(frozen=True)
class OrderSummary:
    id: int
    customer_id: int
    line_count: int


class OrderRepository(Protocol):
    async def add(self, customer_id: int, lines: Sequence[tuple[str, int]]) -> int: ...

    async def get(self, order_id: int) -> OrderSummary | None: ...

    async def list_by_customer(self, customer_id: int) -> list[OrderSummary]: ...


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._rows: dict[int, OrderSummary] = {}
        self._next_id = 1

    async def add(self, customer_id: int, lines: Sequence[tuple[str, int]]) -> int:
        summary = OrderSummary(
            id=self._next_id, customer_id=customer_id, line_count=len(lines)
        )
        self._rows[summary.id] = summary
        self._next_id += 1
        return summary.id

    async def get(self, order_id: int) -> OrderSummary | None:
        return self._rows.get(order_id)

    async def list_by_customer(self, customer_id: int) -> list[OrderSummary]:
        return sorted(
            (r for r in self._rows.values() if r.customer_id == customer_id),
            key=lambda r: r.id,
        )


class SqlOrderRepository:
    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = sessions

    async def add(self, customer_id: int, lines: Sequence[tuple[str, int]]) -> int:
        async with self._sessions() as session, session.begin():
            order = Order(customer_id=customer_id)
            order.lines = [OrderLine(sku=sku, qty=qty) for sku, qty in lines]
            session.add(order)
            await session.flush()
            return order.id

    async def get(self, order_id: int) -> OrderSummary | None:
        async with self._sessions() as session:
            stmt = (
                select(Order)
                .where(Order.id == order_id)
                .options(selectinload(Order.lines))
            )
            order = (await session.scalars(stmt)).one_or_none()
            if order is None:
                return None
            return OrderSummary(order.id, order.customer_id, len(order.lines))

    async def list_by_customer(self, customer_id: int) -> list[OrderSummary]:
        async with self._sessions() as session:
            stmt = (
                select(Order)
                .where(Order.customer_id == customer_id)
                .options(selectinload(Order.lines))
                .order_by(Order.id.asc())
            )
            orders = (await session.scalars(stmt)).all()
            return [OrderSummary(o.id, o.customer_id, len(o.lines)) for o in orders]
