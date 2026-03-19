from unittest.mock import MagicMock

import pytest

from src.domain.models.ship import CargoHold, Ship
from src.infrastructure.adapters.outbound.persistence.mongo_ship_repository import MongoShipRepository


def _make_ship(ship_id: str = "507f1f77bcf86cd799439011") -> Ship:
    return Ship(
        id=ship_id,
        name="Aurora",
        manufacturer="RSI",
        cargo_holds=[CargoHold(name="Main", volume_scu=10.0)],
        total_scu=10.0,
        scm_speed=200.0,
        quantum_speed=500.0,
        landing_time_seconds=60.0,
        loading_time_per_scu_seconds=5.0,
    )


def _make_doc(ship_id: str = "507f1f77bcf86cd799439011") -> dict:
    from bson import ObjectId

    return {
        "_id": ObjectId(ship_id),
        "name": "Aurora",
        "manufacturer": "RSI",
        "cargo_holds": [{"name": "Main", "volume_scu": 10.0}],
        "total_scu": 10.0,
        "scm_speed": 200.0,
        "quantum_speed": 500.0,
        "landing_time_seconds": 60.0,
        "loading_time_per_scu_seconds": 5.0,
    }


@pytest.fixture
def mock_collection() -> MagicMock:
    return MagicMock()


@pytest.fixture
def repo(mock_collection: MagicMock) -> MongoShipRepository:
    return MongoShipRepository(collection=mock_collection)


class TestSearchByName:
    def test_search_returns_matching_ships(self, repo: MongoShipRepository, mock_collection: MagicMock) -> None:
        doc = _make_doc()
        mock_collection.find.return_value = [doc]

        results = repo.search_by_name("aurora")

        mock_collection.find.assert_called_once_with({"name": {"$regex": "aurora", "$options": "i"}})
        assert len(results) == 1
        assert results[0].name == "Aurora"

    def test_search_returns_empty_when_no_match(self, repo: MongoShipRepository, mock_collection: MagicMock) -> None:
        mock_collection.find.return_value = []

        results = repo.search_by_name("nonexistent")

        assert results == []

    def test_search_passes_query_to_regex(self, repo: MongoShipRepository, mock_collection: MagicMock) -> None:
        mock_collection.find.return_value = []

        repo.search_by_name("Zeus")

        mock_collection.find.assert_called_once_with({"name": {"$regex": "Zeus", "$options": "i"}})


class TestUpdate:
    def test_update_returns_ship_on_success(self, repo: MongoShipRepository, mock_collection: MagicMock) -> None:
        ship = _make_ship()
        mock_result = MagicMock()
        mock_result.matched_count = 1
        mock_collection.replace_one.return_value = mock_result

        result = repo.update(ship)

        assert result == ship

    def test_update_returns_none_when_not_found(self, repo: MongoShipRepository, mock_collection: MagicMock) -> None:
        ship = _make_ship()
        mock_result = MagicMock()
        mock_result.matched_count = 0
        mock_collection.replace_one.return_value = mock_result

        result = repo.update(ship)

        assert result is None

    def test_update_calls_replace_one_with_correct_filter(
        self, repo: MongoShipRepository, mock_collection: MagicMock
    ) -> None:
        from bson import ObjectId

        ship = _make_ship()
        mock_result = MagicMock()
        mock_result.matched_count = 1
        mock_collection.replace_one.return_value = mock_result

        repo.update(ship)

        call_args = mock_collection.replace_one.call_args
        assert call_args[0][0] == {"_id": ObjectId(ship.id)}
