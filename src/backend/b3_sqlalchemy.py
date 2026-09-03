"""B3 · SQLAlchemy 2.0   (docs/36_backend_B3.md)

2.0 스타일은 **타입 힌트가 곧 컬럼 정의**입니다.
`Mapped[str]` 이면 NOT NULL, `Mapped[str | None]` 이면 nullable. mypy 도 그대로 이해합니다.

실습은 인메모리 SQLite(aiosqlite)로 돕니다 — DB 설치 없이 진짜 쿼리가 나갑니다.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Protocol

from sqlalchemy import Select, event
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ── 이건 이미 돼 있습니다 — 엔진·스키마·쿼리 카운터 ─────────


class Base(DeclarativeBase):
    pass


def make_engine(url: str = "sqlite+aiosqlite:///:memory:", echo: bool = False) -> AsyncEngine:
    from sqlalchemy.ext.asyncio import create_async_engine

    return create_async_engine(url, echo=echo)


def make_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    # expire_on_commit=False: 커밋 뒤에도 객체 속성을 다시 조회하지 않는다.
    # True 로 두면 비동기 환경에서 재조회가 MissingGreenlet 오류로 터진다.
    return async_sessionmaker(engine, expire_on_commit=False)


async def setup_schema(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@contextmanager
def count_queries(engine: AsyncEngine) -> Iterator[list[str]]:
    """블록 안에서 실제로 나간 SQL 문을 모아 준다.

    `echo=True` 로 눈으로 세는 대신 테스트로 세기 위한 장치입니다.
    N+1 은 "느리다"가 아니라 "쿼리 수가 행 수에 비례한다"로 잡아야 재발을 막습니다.
    """
    statements: list[str] = []

    def before(conn, cursor, statement, parameters, context, executemany):  # noqa: ANN001
        statements.append(statement)

    event.listen(engine.sync_engine, "before_cursor_execute", before)
    try:
        yield statements
    finally:
        event.remove(engine.sync_engine, "before_cursor_execute", before)


# ── DRILL B3-1 · 모델 정의 ──────────────────────────────────


class Product(Base):
    """상품. **여기부터 직접 만드세요.**

        __tablename__ = "products"
    # 기본키만 미리 둡니다(이게 없으면 임포트 자체가 안 됩니다). 나머지는 직접.
    id: Mapped[int] = mapped_column(primary_key=True)
        id:    Mapped[int] = mapped_column(primary_key=True)
        sku:   Mapped[str] = mapped_column(String(64), unique=True)
        name:  Mapped[str] = mapped_column(String(200))
        stock: Mapped[int]
    """

    __tablename__ = "products"
    # 기본키만 미리 둡니다(이게 없으면 임포트 자체가 안 됩니다). 나머지는 직접.
    id: Mapped[int] = mapped_column(primary_key=True)


class Order(Base):
    """주문.

        __tablename__ = "orders"
    # 기본키만 미리 둡니다(이게 없으면 임포트 자체가 안 됩니다). 나머지는 직접.
    id: Mapped[int] = mapped_column(primary_key=True)
        id:          Mapped[int]      기본키
        customer_id: Mapped[int]      index=True
        created_at:  Mapped[datetime] server_default=func.now()
        lines:       Mapped[list["OrderLine"]] = relationship(
                         back_populates="order",
                         cascade="all, delete-orphan",
                         lazy="raise",
                     )

    ⚠️ `lazy="raise"` 가 이 파트의 핵심입니다.
       지연 로딩을 **금지**해 두면, 실수로 N+1을 만들었을 때 조용히 느려지는 대신
       개발 중에 예외가 터져 바로 잡힙니다. 비동기 세션에서는 지연 로딩이 애초에
       불가능하므로 더더욱 이렇게 두는 편이 낫습니다.
    """

    __tablename__ = "orders"
    # 기본키만 미리 둡니다(이게 없으면 임포트 자체가 안 됩니다). 나머지는 직접.
    id: Mapped[int] = mapped_column(primary_key=True)


class OrderLine(Base):
    """주문 라인.

        __tablename__ = "order_lines"
    # 기본키만 미리 둡니다(이게 없으면 임포트 자체가 안 됩니다). 나머지는 직접.
    id: Mapped[int] = mapped_column(primary_key=True)
        id:       Mapped[int]  기본키
        order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
        sku:      Mapped[str] = mapped_column(String(64))
        qty:      Mapped[int]
        order:    Mapped[Order] = relationship(back_populates="lines")
    """

    __tablename__ = "order_lines"
    # 기본키만 미리 둡니다(이게 없으면 임포트 자체가 안 됩니다). 나머지는 직접.
    id: Mapped[int] = mapped_column(primary_key=True)


# ── DRILL B3-2 · N+1 없이 조회하기 ──────────────────────────


async def orders_with_lines(session: AsyncSession, customer_id: int) -> list[Order]:
    """한 고객의 주문을 **라인까지 함께** 가져온다. id 내림차순.

    반환된 Order 의 `.lines` 에 접근해도 추가 쿼리가 나가지 않아야 하고,
    lazy="raise" 때문에 예외가 나서도 안 됩니다.

    `.options(selectinload(Order.lines))` 를 쓰면 주문 조회 1번 + 라인 IN 조회 1번,
    총 **2번**으로 끝납니다. 테스트가 쿼리 수를 셉니다.

    joinedload 와의 차이도 직접 비교해 보세요:
      selectinload — 쿼리 2번, 각각 단순. 컬렉션(1:N)에 유리
      joinedload   — 쿼리 1번, LEFT JOIN 이라 부모 행이 자식 수만큼 중복 전송
    """
    raise NotImplementedError


async def order_counts_by_customer(
    session: AsyncSession, min_orders: int
) -> list[tuple[int, int]]:
    """주문이 min_orders 건 이상인 고객만 (customer_id, 주문수) 로 집계한다.

    건수 내림차순, 같으면 customer_id 오름차순.

    파이썬으로 다 가져와서 세지 말고 `func.count()` + `group_by` + `having` 으로
    DB에서 집계하세요. 10만 건이 되는 순간 결과가 갈립니다.
    """
    raise NotImplementedError


# ── DRILL B3-3 · 경쟁 조건과 행 잠금 ────────────────────────


class OutOfStockError(Exception):
    """재고가 모자랄 때."""


class ProductNotFoundError(Exception):
    """상품이 없을 때."""


def stock_lock_stmt(product_id: int) -> Select[tuple[Product]]:
    """해당 상품 행을 **잠그면서** 읽는 SELECT 문을 만들어 돌려준다.

        select(Product).where(Product.id == product_id).with_for_update()

    문(statement)만 만들고 실행하지 않습니다. 그래야 테스트가 "정말 FOR UPDATE 가
    붙었는지"를 SQL로 확인할 수 있습니다.

    ⚠️ SQLite 는 FOR UPDATE 를 지원하지 않아 조용히 무시합니다. 그래서 여기서는
       PostgreSQL 방언으로 컴파일해 검증합니다. 실제 경쟁 조건 재현은 Postgres 로
       직접 해 보세요 — 두 세션을 열고 같은 재고를 동시에 깎으면 잠금 없이는
       둘 다 성공해 재고가 음수가 됩니다.
    """
    raise NotImplementedError


async def decrement_stock(session: AsyncSession, product_id: int, qty: int) -> int:
    """재고를 qty 만큼 깎고 남은 재고를 돌려준다.

    - 상품이 없으면 ProductNotFoundError
    - 재고가 모자라면 OutOfStockError (재고는 그대로)
    - 반드시 stock_lock_stmt 로 **읽으면서 잠근** 뒤 계산하세요.
      "읽고 → 계산하고 → 쓰기" 사이에 다른 트랜잭션이 끼어드는 것이 바로 그 경쟁 조건입니다.

    commit 은 호출한 쪽이 합니다(트랜잭션 경계는 이 함수가 정하지 않습니다).
    """
    raise NotImplementedError


# ── DRILL B3-4 · 리포지터리를 Protocol 로 ───────────────────


@dataclass(frozen=True)
class OrderSummary:
    id: int
    customer_id: int
    line_count: int


class OrderRepository(Protocol):
    """주문 저장소 인터페이스. **Protocol 로 정의하세요** (지금은 뼈대만 있습니다).

    ABC 와 달리 Protocol 은 **상속을 요구하지 않습니다**. 모양만 맞으면 그 타입입니다.
    덕분에 인메모리 구현이 SQLAlchemy 를 전혀 몰라도 되고, 테스트가 빨라집니다.

    메서드 세 개:
        async def add(self, customer_id: int, lines: Sequence[tuple[str, int]]) -> int
            주문을 저장하고 새 id 를 돌려준다. lines 는 (sku, qty) 쌍들.
        async def get(self, order_id: int) -> OrderSummary | None
        async def list_by_customer(self, customer_id: int) -> list[OrderSummary]
            id 오름차순.
    """


class InMemoryOrderRepository:
    """테스트용 인메모리 구현. DB 없이 돕니다."""

    def __init__(self) -> None:
        raise NotImplementedError


class SqlOrderRepository:
    """SQLAlchemy 구현. 생성자로 async_sessionmaker 를 받습니다.

        def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None: ...

    ⚠️ 두 구현은 **같은 테스트를 통과해야 합니다.** 테스트가 두 개를 번갈아 돌립니다.
       그게 "교체 가능하다"의 진짜 의미입니다 — 인터페이스만 같은 게 아니라
       동작이 같아야 바꿔 끼울 수 있습니다.
    """

    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        raise NotImplementedError
