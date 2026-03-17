import time
from unittest.mock import MagicMock, patch

import jwt
import pytest
from fastapi.testclient import TestClient

from src.domain.models.ship import Ship
from src.infrastructure.adapters.inbound.api.ship_router import _CACHE_MAX_AGE

_JWT_SECRET = "test-secret-key-at-least-32-bytes-long"


def _make_token(permissions: list[str] | None = None) -> str:
    payload = {
        "sub": "user-1",
        "username": "testuser",
        "permissions": permissions or [],
        "exp": int(time.time()) + 3600,
    }
    return jwt.encode(payload, _JWT_SECRET, algorithm="HS256")


def _auth_header(permissions: list[str] | None = None) -> dict[str, str]:
    return {"Authorization": f"Bearer {_make_token(permissions)}"}


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock()


@pytest.fixture
def client(mock_service: MagicMock) -> TestClient:
    with (
        patch.dict("os.environ", {"HEXADIAN_AUTH_JWT_SECRET": _JWT_SECRET}),
        patch("src.infrastructure.config.dependencies.MongoClient"),
    ):
        from src.main import create_app

        app = create_app()

    from src.infrastructure.adapters.inbound.api import ship_router

    ship_router._ship_service = mock_service
    return TestClient(app)


def _make_ship() -> Ship:
    return Ship(id="abc123", name="Aurora", manufacturer="RSI")


class TestGetShipCacheHeader:
    def test_get_ship_has_cache_control(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.get.return_value = _make_ship()

        response = client.get("/ships/abc123", headers=_auth_header(["hhh:ships:read"]))

        assert response.status_code == 200
        assert response.headers["cache-control"] == f"max-age={_CACHE_MAX_AGE}"

    def test_list_ships_has_cache_control(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.list_all.return_value = [_make_ship()]

        response = client.get("/ships/", headers=_auth_header(["hhh:ships:read"]))

        assert response.status_code == 200
        assert response.headers["cache-control"] == f"max-age={_CACHE_MAX_AGE}"

    def test_create_ship_no_cache_control(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.create.return_value = _make_ship()

        response = client.post(
            "/ships/", json={"name": "Aurora", "manufacturer": "RSI"}, headers=_auth_header(["hhh:ships:write"])
        )

        assert response.status_code == 201
        assert "cache-control" not in response.headers

    def test_delete_ship_no_cache_control(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.delete.return_value = True

        response = client.delete("/ships/abc123", headers=_auth_header(["hhh:ships:delete"]))

        assert response.status_code == 204
        assert "cache-control" not in response.headers


class TestHealthEndpoint:
    def test_health_is_public(self, client: TestClient) -> None:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestAuthenticationRequired:
    def test_get_ship_requires_auth(self, client: TestClient) -> None:
        response = client.get("/ships/abc123")

        assert response.status_code == 401

    def test_list_ships_requires_auth(self, client: TestClient) -> None:
        response = client.get("/ships/")

        assert response.status_code == 401

    def test_create_ship_requires_auth(self, client: TestClient) -> None:
        response = client.post("/ships/", json={"name": "Aurora", "manufacturer": "RSI"})

        assert response.status_code == 401

    def test_delete_ship_requires_auth(self, client: TestClient) -> None:
        response = client.delete("/ships/abc123")

        assert response.status_code == 401

    def test_expired_token_returns_401(self, client: TestClient) -> None:
        payload = {
            "sub": "user-1",
            "username": "testuser",
            "permissions": ["hhh:ships:read"],
            "exp": int(time.time()) - 3600,
        }
        token = jwt.encode(payload, _JWT_SECRET, algorithm="HS256")

        response = client.get("/ships/abc123", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 401


class TestPermissionRequired:
    def test_create_ship_forbidden_without_write(self, client: TestClient) -> None:
        response = client.post(
            "/ships/",
            json={"name": "Aurora", "manufacturer": "RSI"},
            headers=_auth_header(["hhh:ships:read"]),
        )

        assert response.status_code == 403

    def test_get_ship_forbidden_without_read(self, client: TestClient) -> None:
        response = client.get("/ships/abc123", headers=_auth_header(["hhh:ships:write"]))

        assert response.status_code == 403

    def test_list_ships_forbidden_without_read(self, client: TestClient) -> None:
        response = client.get("/ships/", headers=_auth_header(["hhh:ships:write"]))

        assert response.status_code == 403

    def test_delete_ship_forbidden_without_delete(self, client: TestClient) -> None:
        response = client.delete("/ships/abc123", headers=_auth_header(["hhh:ships:read"]))

        assert response.status_code == 403
