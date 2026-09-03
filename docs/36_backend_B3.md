# B3 · SQLAlchemy 2.0

`선언적 모델 · select · 세션 · N+1`

*모델 정의*

```python
from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase): pass

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(index=True)
    memo: Mapped[str | None] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    lines: Mapped[list["OrderLine"]] = relationship(
        back_populates="order", cascade="all, delete-orphan", lazy="raise"
    )

class OrderLine(Base):
    __tablename__ = "order_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    sku: Mapped[str]
    qty: Mapped[int]

    order: Mapped[Order] = relationship(back_populates="lines")
```

2.0 스타일은 **타입 힌트가 컬럼 정의**입니다. `Mapped[str | None]`이면 nullable, `Mapped[str]`이면 NOT NULL. mypy도 그대로 이해합니다.

*조회*

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

stmt = (
    select(Order)
    .where(Order.customer_id == 42, Order.created_at >= since)
    .options(selectinload(Order.lines))       # N+1 방지: 별도 IN 쿼리 한 번
    .order_by(Order.created_at.desc())
    .limit(20)
)
orders = (await session.scalars(stmt)).all()

# 집계
stmt = (
    select(Order.customer_id, func.count().label("cnt"), func.sum(OrderLine.qty))
    .join(OrderLine)
    .group_by(Order.customer_id)
    .having(func.count() > 3)
)
rows = (await session.execute(stmt)).all()    # Row 튜플들
```

**⚠️ Gotcha · N+1**

지연 로딩 관계를 루프에서 접근하면 쿼리가 행 수만큼 나갑니다. 위 모델처럼 `lazy="raise"`를 기본으로 걸어 두면 **실수로 지연 로딩할 때 예외가 나서** 개발 중에 바로 잡힙니다. 필요한 곳에서만 `selectinload`/`joinedload`를 명시하세요. 비동기 세션에서는 지연 로딩이 아예 불가능하므로 더더욱 중요합니다.

*세션과 트랜잭션*

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(settings.database_url, pool_size=10, max_overflow=20,
                             pool_pre_ping=True, echo=settings.debug)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def create_order(payload: OrderCreate) -> Order:
    async with SessionLocal() as session:
        async with session.begin():           # 블록을 벗어나면 commit, 예외면 rollback
            order = Order(customer_id=payload.customer_id)
            order.lines = [OrderLine(sku=l.sku, qty=l.qty) for l in payload.lines]
            session.add(order)
        return order
```

**💡 expire_on_commit=False**

기본값(`True`)에서는 커밋 직후 객체 속성이 만료되어 **접근할 때마다 다시 쿼리**합니다. 비동기 환경에서는 그 재조회가 실패해 `MissingGreenlet` 오류로 나타납니다. FastAPI 조합에서는 거의 항상 `False`로 둡니다.

**☕ JVM 개발자 노트**

Session ≈ JPA `EntityManager`, identity map·더티 체킹·플러시 개념이 그대로 있습니다. 차이는 **트랜잭션 경계를 어노테이션이 아니라 `async with session.begin()` 블록으로 직접 긋는다**는 점입니다. `@Transactional`의 프록시 함정(같은 클래스 내부 호출 시 미적용) 같은 게 없어 오히려 예측 가능합니다. 마이그레이션은 Flyway 대신 **alembic**입니다.

### 🏋 DRILL B3 — SQLAlchemy

1. 주문·주문라인·상품 3개 테이블을 정의하고 alembic으로 초기 마이그레이션을 생성하세요.
2. 일부러 N+1을 만들고 `echo=True`로 쿼리 수를 센 뒤, `selectinload`와 `joinedload`를 각각 적용해 쿼리 형태를 비교하세요.
3. 동시에 같은 재고를 차감하는 두 트랜잭션을 만들어 경쟁 조건을 재현하고, `with_for_update()`로 해결하세요.
4. 리포지터리를 `Protocol`(12파트)로 정의하고 인메모리 구현과 SQLAlchemy 구현을 교체 가능하게 만드세요.
