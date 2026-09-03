"""B3 · SQLAlchemy 채점."""

import pytest

pytest.importorskip("sqlalchemy", reason="uv sync --group backend 를 먼저 실행하세요")
pytest.importorskip("aiosqlite", reason="uv sync --group backend 를 먼저 실행하세요")

from sqlalchemy import select  # noqa: E402
from sqlalchemy.dialects import postgresql  # noqa: E402
from sqlalchemy.exc import InvalidRequestError  # noqa: E402

from backend.b3_sqlalchemy import (  # noqa: E402
    InMemoryOrderRepository,
    Order,
    OrderLine,
    OrderSummary,
    OutOfStockError,
    Product,
    ProductNotFoundError,
    SqlOrderRepository,
    count_queries,
    decrement_stock,
    make_engine,
    make_sessionmaker,
    order_counts_by_customer,
    orders_with_lines,
    setup_schema,
    stock_lock_stmt,
)


@pytest.fixture
async def engine():
    eng = make_engine()
    await setup_schema(eng)
    yield eng
    await eng.dispose()


@pytest.fixture
def sessions(engine):
    return make_sessionmaker(engine)


@pytest.fixture
async def seeded(engine, sessions):
    """고객 1: 주문 3건(라인 2·1·1), 고객 2: 주문 1건, 상품 2개."""
    async with sessions() as session, session.begin():
        session.add_all([
            Product(sku="P1", name="키보드", stock=10),
            Product(sku="P2", name="마우스", stock=0),
        ])
        session.add(Order(customer_id=1, lines=[OrderLine(sku="P1", qty=1),
                                                OrderLine(sku="P2", qty=2)]))
        session.add(Order(customer_id=1, lines=[OrderLine(sku="P1", qty=3)]))
        session.add(Order(customer_id=1, lines=[OrderLine(sku="P2", qty=1)]))
        session.add(Order(customer_id=2, lines=[OrderLine(sku="P1", qty=5)]))
    return sessions


class TestModels:
    def test_columns_come_from_type_hints(self):
        assert (Product.__tablename__, Order.__tablename__) == ("products", "orders")
        assert OrderLine.__tablename__ == "order_lines"
        assert {"id", "sku", "name", "stock"} <= set(Product.__table__.columns.keys())
        assert {"id", "customer_id", "created_at"} <= set(Order.__table__.columns.keys())
        assert {"id", "order_id", "sku", "qty"} <= set(OrderLine.__table__.columns.keys())

    def test_sku_is_unique_and_foreign_key_is_wired(self):
        assert Product.__table__.columns["sku"].unique is True
        fks = list(OrderLine.__table__.columns["order_id"].foreign_keys)
        assert fks and fks[0].target_fullname == "orders.id"

    def test_lines_relationship_forbids_lazy_loading(self):
        assert Order.lines.property.lazy == "raise"

    async def test_cascade_deletes_orphan_lines(self, seeded, sessions):
        async with sessions() as session, session.begin():
            order = (await orders_with_lines(session, 2))[0]
            await session.delete(order)
        async with sessions() as session:
            remaining = (await session.scalars(select(OrderLine).where(
                OrderLine.sku == "P1", OrderLine.qty == 5))).all()
        assert remaining == []


class TestOrdersWithLines:
    async def test_returns_orders_newest_first(self, seeded, sessions):
        async with sessions() as session:
            orders = await orders_with_lines(session, 1)
        assert [o.customer_id for o in orders] == [1, 1, 1]
        assert [o.id for o in orders] == sorted([o.id for o in orders], reverse=True)

    async def test_lines_are_loaded_eagerly(self, seeded, sessions):
        async with sessions() as session:
            orders = await orders_with_lines(session, 1)
        # 세션을 벗어난 뒤에도 접근된다 — 이미 로딩돼 있다는 뜻
        assert sorted(len(o.lines) for o in orders) == [1, 1, 2]

    async def test_costs_exactly_two_queries_not_n_plus_1(self, seeded, sessions, engine):
        with count_queries(engine) as sql:
            async with sessions() as session:
                orders = await orders_with_lines(session, 1)
                _ = [len(o.lines) for o in orders]
        selects = [s for s in sql if s.lstrip().upper().startswith("SELECT")]
        assert len(selects) == 2, (
            f"쿼리 {len(selects)}번 — selectinload 를 빠뜨렸거나 라인마다 조회하고 있습니다"
        )

    async def test_without_eager_loading_it_raises(self, seeded, sessions):
        # lazy="raise" 가 하는 일: 조용한 N+1 대신 즉시 실패
        async with sessions() as session:
            order = (await session.scalars(select(Order).limit(1))).one()
            with pytest.raises(InvalidRequestError):
                _ = order.lines

    async def test_unknown_customer_is_empty(self, seeded, sessions):
        async with sessions() as session:
            assert await orders_with_lines(session, 999) == []


class TestOrderCountsByCustomer:
    async def test_aggregates_and_filters(self, seeded, sessions):
        async with sessions() as session:
            assert await order_counts_by_customer(session, 1) == [(1, 3), (2, 1)]

    async def test_having_excludes_small_customers(self, seeded, sessions):
        async with sessions() as session:
            assert await order_counts_by_customer(session, 2) == [(1, 3)]

    async def test_aggregation_happens_in_the_database(self, seeded, sessions, engine):
        with count_queries(engine) as sql:
            async with sessions() as session:
                await order_counts_by_customer(session, 1)
        joined = " ".join(sql).upper()
        assert "GROUP BY" in joined and "COUNT" in joined   # 파이썬에서 세면 실패한다

    async def test_no_match(self, seeded, sessions):
        async with sessions() as session:
            assert await order_counts_by_customer(session, 99) == []


class TestStockLock:
    def test_statement_renders_for_update(self):
        sql = str(stock_lock_stmt(1).compile(dialect=postgresql.dialect()))
        assert "FOR UPDATE" in sql.upper()

    def test_targets_a_single_product(self):
        sql = str(stock_lock_stmt(1).compile(dialect=postgresql.dialect()))
        assert "products" in sql.lower()

    async def test_decrements_and_returns_remaining(self, seeded, sessions):
        async with sessions() as session, session.begin():
            product = (await session.scalars(select(Product).where(Product.sku == "P1"))).one()
            assert await decrement_stock(session, product.id, 4) == 6

    async def test_persists(self, seeded, sessions):
        async with sessions() as session, session.begin():
            product = (await session.scalars(select(Product).where(Product.sku == "P1"))).one()
            await decrement_stock(session, product.id, 4)
            pid = product.id
        async with sessions() as session:
            assert (await session.get(Product, pid)).stock == 6

    async def test_out_of_stock_leaves_it_untouched(self, seeded, sessions):
        async with sessions() as session:
            product = (await session.scalars(select(Product).where(Product.sku == "P2"))).one()
            with pytest.raises(OutOfStockError):
                await decrement_stock(session, product.id, 1)
        async with sessions() as session:
            assert (await session.scalars(
                select(Product).where(Product.sku == "P2"))).one().stock == 0

    async def test_missing_product(self, seeded, sessions):
        async with sessions() as session:
            with pytest.raises(ProductNotFoundError):
                await decrement_stock(session, 9999, 1)


class TestRepositoriesAreInterchangeable:
    """같은 테스트를 인메모리 구현과 SQLAlchemy 구현에 **둘 다** 돌린다.

    인터페이스만 같은 게 아니라 동작이 같아야 진짜 교체 가능한 것입니다.
    """

    @pytest.fixture(params=["memory", "sql"])
    async def repo(self, request, engine, sessions):
        if request.param == "memory":
            return InMemoryOrderRepository()
        return SqlOrderRepository(sessions)

    async def test_add_returns_a_new_id(self, repo):
        first = await repo.add(1, [("P1", 2)])
        second = await repo.add(1, [("P2", 1)])
        assert first != second

    async def test_get_reads_back_the_summary(self, repo):
        order_id = await repo.add(7, [("P1", 2), ("P2", 3)])
        summary = await repo.get(order_id)
        assert summary == OrderSummary(id=order_id, customer_id=7, line_count=2)

    async def test_get_missing_is_none(self, repo):
        assert await repo.get(99999) is None

    async def test_list_by_customer_is_ordered_and_filtered(self, repo):
        a = await repo.add(1, [("P1", 1)])
        await repo.add(2, [("P1", 1)])
        b = await repo.add(1, [("P2", 1)])
        assert [s.id for s in await repo.list_by_customer(1)] == [a, b]

    async def test_list_by_unknown_customer_is_empty(self, repo):
        assert await repo.list_by_customer(999) == []

    async def test_in_memory_does_not_touch_sqlalchemy(self):
        repo = InMemoryOrderRepository()
        await repo.add(1, [("P1", 1)])
        assert (await repo.get(1)).line_count == 1     # DB 없이 돈다
