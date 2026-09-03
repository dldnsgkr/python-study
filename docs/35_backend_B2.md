# B2 · FastAPI — 타입이 곧 API 스펙

`routing · Depends · 예외 · 테스트`

*최소 구조*

```text
from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from fastapi.responses import JSONResponse

app = FastAPI(title="Order API", version="1.0.0")

@app.get("/orders/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int = Path(gt=0),
    include_lines: bool = Query(default=False),
    service: OrderService = Depends(get_order_service),
):
    order = await service.get(order_id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="주문을 찾을 수 없습니다")
    return order

@app.post("/orders", response_model=OrderRead, status_code=201)
async def create_order(payload: OrderCreate, service: OrderService = Depends(get_order_service)):
    return await service.create(payload)
```

여기서 **타입 힌트가 전부**를 결정합니다. 경로 파라미터 파싱, 쿼리 파라미터 기본값, 본문 검증, 응답 직렬화, OpenAPI 문서(`/docs`)까지 전부 시그니처에서 나옵니다.

## 의존성 주입

*Depends*

```python
from typing import Annotated

async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session                    # 요청 끝나면 자동 정리 (11파트 컨텍스트 매니저)

SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: SessionDep) -> User:
    user = await find_user_by_token(session, token)
    if user is None:
        raise HTTPException(401, "인증이 필요합니다")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/me")
async def me(user: CurrentUser):        # 의존성이 중첩돼도 캐시되어 한 번만 실행
    return user
```

**☕ JVM 개발자 노트**

`Depends`는 스프링의 생성자 주입과 달리 **요청 스코프**가 기본이고, 컨테이너가 아니라 **함수 시그니처**가 의존성 그래프입니다. `Annotated` 별칭(`SessionDep`)을 만들어 두는 것이 실무 관례입니다. 같은 요청 안에서 같은 의존성은 캐시되므로 스프링의 싱글턴/프로토타입 개념과 혼동하지 마세요.

*예외 처리와 수명주기*

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await create_pool()      # 시작 시
    yield
    await app.state.pool.close()              # 종료 시

app = FastAPI(lifespan=lifespan)

@app.exception_handler(DomainError)           # 13파트의 루트 예외를 여기서 한 번에 변환
async def domain_error_handler(request, exc: DomainError):
    return JSONResponse(status_code=400, content={"code": exc.code, "message": str(exc)})
```

**⚠️ Gotcha**

`async def` 핸들러 안에서 동기 블로킹 호출(예: 동기 DB 드라이버, `requests`)을 하면 **이벤트 루프 전체가 멈춥니다**(17파트). 동기 라이브러리를 써야 하면 핸들러를 그냥 `def`로 선언하세요 — FastAPI가 자동으로 스레드풀에서 실행합니다. 최악은 `async def` + 동기 블로킹 조합입니다.

*테스트*

```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.fixture
async def client():
    app.dependency_overrides[get_order_service] = lambda: FakeOrderService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

async def test_get_order_404(client):
    resp = await client.get("/orders/999")
    assert resp.status_code == 404
```

`dependency_overrides`는 FastAPI 테스트의 핵심입니다. 몽키패치 없이 **의존성 그래프의 노드만 교체**합니다(18파트의 mock보다 훨씬 안정적입니다).

### 🏋 DRILL B2 — FastAPI

1. 주문 CRUD 5개 엔드포인트를 만들고 `/docs`에서 스키마가 정확히 생성되는지 확인하세요.
2. 도메인 예외 계층(13파트)을 만들고 예외 핸들러 하나로 HTTP 상태 코드를 매핑하세요.
3. 커서 기반 페이지네이션(`?cursor=&limit=`)을 응답 모델과 함께 구현하세요.
4. `async def` 핸들러에서 `time.sleep(3)`을 호출하고 동시 요청 10개를 보내 총 소요 시간을 측정한 뒤, `def`로 바꿔 다시 측정해 차이를 확인하세요.
