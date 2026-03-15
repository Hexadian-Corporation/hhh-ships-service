from unittest.mock import MagicMock

import pytest

from src.application.ports.outbound.ship_repository import ShipRepository
from src.application.services.ship_service_impl import ShipServiceImpl
from src.domain.models.ship import Ship


@pytest.fixture
def mock_repo() -> MagicMock:
    return MagicMock(spec=ShipRepository)


@pytest.fixture
def service(mock_repo: MagicMock) -> ShipServiceImpl:
    return ShipServiceImpl(ship_repository=mock_repo)


def _make_ship(ship_id: str = "abc123", name: str = "Aurora") -> Ship:
    return Ship(id=ship_id, name=name, manufacturer="RSI")


class TestGetShip:
    def test_get_ship_calls_repo(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ship = _make_ship()
        mock_repo.find_by_id.return_value = ship

        result = service.get_ship("abc123")

        assert result == ship
        mock_repo.find_by_id.assert_called_once_with("abc123")

    def test_get_ship_caches_result(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ship = _make_ship()
        mock_repo.find_by_id.return_value = ship

        service.get_ship("abc123")
        service.get_ship("abc123")

        mock_repo.find_by_id.assert_called_once()

    def test_get_ship_returns_none_not_cached(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        mock_repo.find_by_id.return_value = None

        result = service.get_ship("missing")

        assert result is None
        mock_repo.find_by_id.assert_called_once()

    def test_get_ship_none_not_cached_on_retry(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        mock_repo.find_by_id.return_value = None

        service.get_ship("missing")
        service.get_ship("missing")

        assert mock_repo.find_by_id.call_count == 2


class TestListShips:
    def test_list_ships_calls_repo(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ships = [_make_ship()]
        mock_repo.find_all.return_value = ships

        result = service.list_ships()

        assert result == ships
        mock_repo.find_all.assert_called_once()

    def test_list_ships_caches_result(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        mock_repo.find_all.return_value = [_make_ship()]

        service.list_ships()
        service.list_ships()

        mock_repo.find_all.assert_called_once()


class TestCreateShip:
    def test_create_ship_delegates_to_repo(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ship = _make_ship(ship_id=None)
        saved = _make_ship()
        mock_repo.save.return_value = saved

        result = service.create_ship(ship)

        assert result == saved
        mock_repo.save.assert_called_once_with(ship)

    def test_create_ship_invalidates_cache(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        mock_repo.find_all.return_value = [_make_ship()]
        service.list_ships()

        mock_repo.save.return_value = _make_ship()
        service.create_ship(_make_ship(ship_id=None))

        service.list_ships()
        assert mock_repo.find_all.call_count == 2


class TestDeleteShip:
    def test_delete_ship_delegates_to_repo(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        mock_repo.delete.return_value = True

        result = service.delete_ship("abc123")

        assert result is True
        mock_repo.delete.assert_called_once_with("abc123")

    def test_delete_ship_invalidates_cache(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ship = _make_ship()
        mock_repo.find_by_id.return_value = ship
        service.get_ship("abc123")

        mock_repo.delete.return_value = True
        service.delete_ship("abc123")

        service.get_ship("abc123")
        assert mock_repo.find_by_id.call_count == 2
