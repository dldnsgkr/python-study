"""B2 · FastAPI 채점."""

import asyncio
import time

import pytest

pytest.importorskip("fastapi", reason="uv sync --group backend 를 먼저 실행하세요")
pytest.importorskip("httpx", reason="uv sync --group backend 를 먼저 실행하세요")

from httpx import ASGITransport, AsyncClient  # noqa: E402

from backend.b2_fastapi import (  # noqa: E402
    ConflictError,
    DomainError,
    NotFoundError,
    OrderRepo,
    create_app,
    create_blocking_app,
)


@pytest.fixture
def repo():
    return OrderRepo()


@pytest.fixture
async def client(repo):
    app = create_app(repo)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestDomainErrors:
    def test_codes_and_statuses(self):
        assert issubclass(NotFoundError, DomainError)
        assert issubclass(ConflictError, DomainError)
        assert (NotFoundError.code, NotFoundError.status) == ("not_found", 404)
        assert (ConflictError.code, ConflictError.status) == ("conflict", 409)
        assert (DomainError.code, DomainError.status) == ("domain_error", 400)

    def test_one_handler_can_catch_them_all(self):
        try:
            raise NotFoundError("없음")
        except DomainError as exc:          # 루트 예외 하나로 전부 잡힌다
            assert exc.status == 404


class TestCreate:
    async def test_returns_201_and_the_created_order(self, client):
        resp = await client.post("/orders", json={"customer_id": 42, "memo": "급함"})
        assert resp.status_code == 201
        body = resp.json()
        assert body["customer_id"] == 42
        assert body["memo"] == "급함"
        assert body["id"] >= 1

    async def test_memo_is_optional(self, client):
        resp = await client.post("/orders", json={"customer_id": 1})
        assert resp.status_code == 201
        assert resp.json()["memo"] is None

    async def test_invalid_body_is_422(self, client):
        resp = await client.post("/orders", json={"customer_id": "숫자아님"})
        assert resp.status_code == 422


class TestGet:
    async def test_reads_back(self, client):
        created = (await client.post("/orders", json={"customer_id": 7})).json()
        resp = await client.get(f"/orders/{created['id']}")
        assert resp.status_code == 200
        assert resp.json() == created

    async def test_missing_order_is_404_with_domain_code(self, client):
        resp = await client.get("/orders/999")
        assert resp.status_code == 404
        assert resp.json()["code"] == "not_found"     # 예외 핸들러를 거쳐 나온 형태
        assert resp.json()["message"]

    @pytest.mark.parametrize("order_id", [0, -1])
    async def test_non_positive_id_is_422_not_404(self, client, order_id):
        resp = await client.get(f"/orders/{order_id}")
        assert resp.status_code == 422                # Path(gt=0) 이 걸러 준다


class TestPagination:
    @pytest.fixture(autouse=True)
    async def _seed(self, client):
        for i in range(25):
            await client.post("/orders", json={"customer_id": i})

    async def test_default_limit_is_10(self, client):
        body = (await client.get("/orders")).json()
        assert len(body["items"]) == 10
        assert body["next_cursor"] == body["items"][-1]["id"]

    async def test_cursor_continues_without_overlap(self, client):
        first = (await client.get("/orders?limit=10")).json()
        second = (await client.get(f"/orders?limit=10&cursor={first['next_cursor']}")).json()
        first_ids = [o["id"] for o in first["items"]]
        second_ids = [o["id"] for o in second["items"]]
        assert set(first_ids) & set(second_ids) == set()
        assert min(second_ids) > max(first_ids)

    async def test_last_page_has_null_cursor(self, client):
        body = (await client.get("/orders?limit=10&cursor=20")).json()
        assert len(body["items"]) == 5
        assert body["next_cursor"] is None            # 여기서 끝이라는 신호

    async def test_limit_bounds_are_enforced(self, client):
        assert (await client.get("/orders?limit=0")).status_code == 422
        assert (await client.get("/orders?limit=101")).status_code == 422

    async def test_custom_limit(self, client):
        body = (await client.get("/orders?limit=3")).json()
        assert len(body["items"]) == 3


class TestPatchAndDelete:
    async def test_patch_updates_memo(self, client):
        created = (await client.post("/orders", json={"customer_id": 1})).json()
        resp = await client.patch(f"/orders/{created['id']}", json={"memo": "변경됨"})
        assert resp.status_code == 200
        assert resp.json()["memo"] == "변경됨"

    async def test_patch_missing_is_404(self, client):
        resp = await client.patch("/orders/999", json={"memo": "x"})
        assert resp.status_code == 404

    async def test_delete_returns_204_with_no_body(self, client):
        created = (await client.post("/orders", json={"customer_id": 1})).json()
        resp = await client.delete(f"/orders/{created['id']}")
        assert resp.status_code == 204
        assert resp.content == b""
        assert (await client.get(f"/orders/{created['id']}")).status_code == 404

    async def test_delete_missing_is_404(self, client):
        assert (await client.delete("/orders/999")).status_code == 404


class TestOpenApi:
    async def test_schema_is_generated_from_the_signatures(self, client):
        schema = (await client.get("/openapi.json")).json()
        assert "/orders" in schema["paths"]
        assert "/orders/{order_id}" in schema["paths"]
        assert set(schema["paths"]["/orders/{order_id}"]) >= {"get", "patch", "delete"}


class TestDependencyOverride:
    async def test_repo_is_injected_and_replaceable(self, repo):
        app = create_app(repo)
        # 앱이 들고 있는 저장소를 통째로 갈아 끼운다 — 몽키패치 없이
        other = OrderRepo()
        other.create(customer_id=999, memo="가짜")
        key = next(iter(app.dependency_overrides))
        app.dependency_overrides[key] = lambda: other
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            body = (await c.get("/orders/1")).json()
        assert body["customer_id"] == 999


class TestBlockingHandler:
    async def test_concurrent_requests_are_not_serialized(self):
        sleep_seconds = 0.1
        app = create_blocking_app(sleep_seconds)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            started = time.perf_counter()
            responses = await asyncio.gather(*(c.get("/report") for _ in range(5)))
            elapsed = time.perf_counter() - started

        assert all(r.status_code == 200 for r in responses)
        # async def + time.sleep 이면 5 * 0.1 = 0.5초가 걸린다.
        # 그냥 def 로 선언하면 스레드풀에서 동시에 돌아 0.1초대에 끝난다.
        assert elapsed < sleep_seconds * 3, (
            f"{elapsed:.2f}초 — 이벤트 루프가 막혔습니다. 핸들러를 async def 로 두고 "
            "time.sleep 을 부르지 않았는지 확인하세요."
        )
