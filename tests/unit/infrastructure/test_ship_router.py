from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.domain.models.ship import Ship
from src.infrastructure.adapters.inbound.api.ship_router import _CACHE_MAX_AGE


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock()


@pytest.fixture
def client(mock_service: MagicMock) -> TestClient:
    with patch("src.infrastructure.config.dependencies.MongoClient"):
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

        response = client.get("/ships/abc123")

        assert response.status_code == 200
        assert response.headers["cache-control"] == f"max-age={_CACHE_MAX_AGE}"

    def test_list_ships_has_cache_control(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.list_all.return_value = [_make_ship()]

        response = client.get("/ships/")

        assert response.status_code == 200
        assert response.headers["cache-control"] == f"max-age={_CACHE_MAX_AGE}"

    def test_create_ship_no_cache_control(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.create.return_value = _make_ship()

        response = client.post("/ships/", json={"name": "Aurora", "manufacturer": "RSI"})

        assert response.status_code == 201
        assert "cache-control" not in response.headers

    def test_delete_ship_no_cache_control(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.delete.return_value = True

        response = client.delete("/ships/abc123")

        assert response.status_code == 204
        assert "cache-control" not in response.headers
