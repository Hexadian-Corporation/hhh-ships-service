from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

_JWT_SECRET = "test-secret-key-at-least-32-bytes-long"


def _make_motor_mock() -> MagicMock:
    """Build a mock AsyncIOMotorClient chain with AsyncMock collection."""
    mock_collection = AsyncMock()
    mock_collection.find = MagicMock()
    mock_collection.find.return_value.to_list = AsyncMock(return_value=[])
    mock_db = MagicMock()
    mock_db.__getitem__ = MagicMock(return_value=mock_collection)
    mock_client = MagicMock()
    mock_client.__getitem__ = MagicMock(return_value=mock_db)
    return mock_client


@pytest.fixture
def client() -> TestClient:
    with (
        patch.dict("os.environ", {"HEXADIAN_AUTH_JWT_SECRET": _JWT_SECRET}),
        patch("src.infrastructure.config.dependencies.AsyncIOMotorClient", return_value=_make_motor_mock()),
    ):
        from src.main import create_app

        app = create_app()
    return TestClient(app, raise_server_exceptions=True)


class TestCORSMiddleware:
    def test_allowed_origin_localhost_3000(self, client: TestClient) -> None:
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )

        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

    def test_allowed_origin_localhost_3001(self, client: TestClient) -> None:
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3001",
                "Access-Control-Request-Method": "GET",
            },
        )

        assert response.headers.get("access-control-allow-origin") == "http://localhost:3001"

    def test_rejected_origin_not_in_allow_list(self, client: TestClient) -> None:
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:9999",
                "Access-Control-Request-Method": "GET",
            },
        )

        assert "access-control-allow-origin" not in response.headers

    def test_get_with_allowed_origin_returns_cors_header(self, client: TestClient) -> None:
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})

        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


class TestLifespan:
    def test_lifespan_calls_seed_ships(self) -> None:
        mock_client = _make_motor_mock()
        with (
            patch.dict("os.environ", {"HEXADIAN_AUTH_JWT_SECRET": _JWT_SECRET}),
            patch("src.infrastructure.config.dependencies.AsyncIOMotorClient", return_value=mock_client),
            patch("src.main.seed_ships") as mock_seed,
        ):
            from src.main import create_app

            app = create_app()

            with TestClient(app):
                pass

        mock_seed.assert_called_once()
