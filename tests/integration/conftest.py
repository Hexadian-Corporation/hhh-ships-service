from collections.abc import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from testcontainers.mongodb import MongoDbContainer

from tests.auth_helpers import _JWT_SECRET


@pytest.fixture(scope="module")
def mongo_container() -> Generator[MongoDbContainer, None, None]:
    with MongoDbContainer("mongo:7") as container:
        yield container


@pytest.fixture(scope="module")
def client(mongo_container: MongoDbContainer) -> Generator[TestClient, None, None]:
    mongo_uri = mongo_container.get_connection_url()

    env = {
        "HEXADIAN_AUTH_JWT_SECRET": _JWT_SECRET,
        "HHH_SHIPS_MONGO_URI": mongo_uri,
        "HHH_SHIPS_MONGO_DB": "test_ships",
    }

    with patch.dict("os.environ", env):
        from src.main import create_app

        app = create_app()

    with TestClient(app) as tc:
        yield tc


@pytest.fixture(autouse=True)
def _clean_collection(mongo_container: MongoDbContainer) -> Generator[None, None, None]:
    """Drop ships collection and clear service cache before each test for full isolation."""
    from pymongo import MongoClient

    from src.infrastructure.adapters.inbound.api import ship_router

    mongo_uri = mongo_container.get_connection_url()
    mc = MongoClient(mongo_uri)
    mc["test_ships"]["ships"].delete_many({})
    mc.close()

    if ship_router._ship_service is not None:
        ship_router._ship_service._cache.clear()

    yield
