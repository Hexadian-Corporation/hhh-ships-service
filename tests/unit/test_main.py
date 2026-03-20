from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

_JWT_SECRET = "test-secret-key-at-least-32-bytes-long"


@pytest.fixture
def client() -> TestClient:
    with (
        patch.dict("os.environ", {"HEXADIAN_AUTH_JWT_SECRET": _JWT_SECRET}),
        patch("src.infrastructure.config.dependencies.MongoClient"),
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
        with (
            patch.dict("os.environ", {"HEXADIAN_AUTH_JWT_SECRET": _JWT_SECRET}),
            patch("src.infrastructure.config.dependencies.MongoClient"),
            patch("src.main.seed_ships") as mock_seed,
        ):
            from src.main import create_app

            app = create_app()

            with TestClient(app):
                pass

        mock_seed.assert_called_once()
