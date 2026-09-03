"""확장 06 · 제어 흐름 채점."""

import hashlib

import pytest

from extra.control import UserError, route, sha256_of


class TestRoute:
    @pytest.mark.parametrize("status", [200, 201])
    def test_success_returns_body(self, status):
        assert route({"status": status, "body": {"id": 1}}) == {"id": 1}

    @pytest.mark.parametrize("status", [400, 404, 422, 499])
    def test_client_error_raises(self, status):
        with pytest.raises(UserError) as info:
            route({"status": status})
        assert info.value.status == status

    @pytest.mark.parametrize("status", [500, 502, 599])
    def test_server_error_asks_for_retry(self, status):
        assert route({"status": status}) == "retry"

    @pytest.mark.parametrize("response", [{"status": 301}, {"status": 100}, {}, {"x": 1}])
    def test_everything_else_is_logged(self, response):
        assert route(response) == "logged"


class TestSha256Of:
    def test_matches_hashlib(self, tmp_path):
        data = b"hello world\n" * 5000
        path = tmp_path / "big.bin"
        path.write_bytes(data)
        assert sha256_of(str(path)) == hashlib.sha256(data).hexdigest()

    def test_empty_file(self, tmp_path):
        path = tmp_path / "empty.bin"
        path.write_bytes(b"")
        assert sha256_of(str(path)) == hashlib.sha256(b"").hexdigest()

    def test_chunk_size_does_not_change_the_result(self, tmp_path):
        path = tmp_path / "x.bin"
        path.write_bytes(b"abcdefghij" * 100)
        assert sha256_of(str(path), 7) == sha256_of(str(path), 4096)
