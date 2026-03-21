from unittest.mock import MagicMock

import pytest

from src.application.ports.outbound.ship_repository import ShipRepository
from src.application.services.ship_service_impl import _CACHE_TTL, ShipServiceImpl
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
    async def test_get_ship_calls_repo(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ship = _make_ship()
        mock_repo.find_by_id.return_value = ship

        result = await service.get("abc123")

        assert result == ship
        mock_repo.find_by_id.assert_called_once_with("abc123")

    async def test_get_ship_caches_result(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ship = _make_ship()
        mock_repo.find_by_id.return_value = ship

        await service.get("abc123")
        await service.get("abc123")

        mock_repo.find_by_id.assert_called_once()

    async def test_get_ship_raises_when_not_found(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        from src.domain.exceptions.ship_exceptions import ShipNotFoundError

        mock_repo.find_by_id.return_value = None

        with pytest.raises(ShipNotFoundError):
            await service.get("missing")

    async def test_get_ship_not_found_not_cached(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        from src.domain.exceptions.ship_exceptions import ShipNotFoundError

        mock_repo.find_by_id.return_value = None

        with pytest.raises(ShipNotFoundError):
            await service.get("missing")
        with pytest.raises(ShipNotFoundError):
            await service.get("missing")

        assert mock_repo.find_by_id.call_count == 2


class TestListShips:
    async def test_list_ships_calls_repo(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ships = [_make_ship()]
        mock_repo.find_all.return_value = ships

        result = await service.list_all()

        assert result == ships
        mock_repo.find_all.assert_called_once()

    async def test_list_ships_caches_result(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        mock_repo.find_all.return_value = [_make_ship()]

        await service.list_all()
        await service.list_all()

        mock_repo.find_all.assert_called_once()


class TestCreateShip:
    async def test_create_ship_delegates_to_repo(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ship = _make_ship(ship_id=None)
        saved = _make_ship()
        mock_repo.save.return_value = saved

        result = await service.create(ship)

        assert result == saved
        mock_repo.save.assert_called_once_with(ship)

    async def test_create_ship_invalidates_cache(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        mock_repo.find_all.return_value = [_make_ship()]
        await service.list_all()

        mock_repo.save.return_value = _make_ship()
        await service.create(_make_ship(ship_id=None))

        await service.list_all()
        assert mock_repo.find_all.call_count == 2


class TestDeleteShip:
    async def test_delete_ship_delegates_to_repo(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        mock_repo.delete.return_value = True

        await service.delete("abc123")

        mock_repo.delete.assert_called_once_with("abc123")

    async def test_delete_ship_raises_when_not_found(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        from src.domain.exceptions.ship_exceptions import ShipNotFoundError

        mock_repo.delete.return_value = False

        with pytest.raises(ShipNotFoundError):
            await service.delete("missing")

    async def test_delete_ship_invalidates_cache(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ship = _make_ship()
        mock_repo.find_by_id.return_value = ship
        await service.get("abc123")

        mock_repo.delete.return_value = True
        await service.delete("abc123")

        await service.get("abc123")
        assert mock_repo.find_by_id.call_count == 2


class TestSearchByName:
    async def test_search_returns_empty_for_blank_query(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        result = await service.search_by_name("")

        assert result == []
        mock_repo.search_by_name.assert_not_called()

    async def test_search_returns_empty_for_whitespace_query(
        self, service: ShipServiceImpl, mock_repo: MagicMock
    ) -> None:
        result = await service.search_by_name("   ")

        assert result == []
        mock_repo.search_by_name.assert_not_called()

    async def test_search_calls_repo(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ships = [_make_ship()]
        mock_repo.search_by_name.return_value = ships

        result = await service.search_by_name("aurora")

        assert result == ships
        mock_repo.search_by_name.assert_called_once_with("aurora")

    async def test_search_caches_result(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        mock_repo.search_by_name.return_value = [_make_ship()]

        await service.search_by_name("aurora")
        await service.search_by_name("aurora")

        mock_repo.search_by_name.assert_called_once()

    async def test_search_cache_is_case_insensitive_key(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        mock_repo.search_by_name.return_value = [_make_ship()]

        await service.search_by_name("Aurora")
        await service.search_by_name("aurora")

        mock_repo.search_by_name.assert_called_once()


class TestUpdateShip:
    async def test_update_ship_raises_if_not_found(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        from src.domain.exceptions.ship_exceptions import ShipNotFoundError

        mock_repo.find_by_id.return_value = None

        with pytest.raises(ShipNotFoundError):
            await service.update(_make_ship())

    async def test_update_ship_raises_if_repo_update_returns_none(
        self, service: ShipServiceImpl, mock_repo: MagicMock
    ) -> None:
        from src.domain.exceptions.ship_exceptions import ShipNotFoundError

        mock_repo.find_by_id.return_value = _make_ship()
        mock_repo.update.return_value = None

        with pytest.raises(ShipNotFoundError):
            await service.update(_make_ship())

    async def test_update_ship_returns_updated(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ship = _make_ship()
        mock_repo.find_by_id.return_value = ship
        mock_repo.update.return_value = ship

        result = await service.update(ship)

        assert result == ship
        mock_repo.update.assert_called_once_with(ship)

    async def test_update_ship_invalidates_cache(self, service: ShipServiceImpl, mock_repo: MagicMock) -> None:
        ship = _make_ship()
        mock_repo.find_all.return_value = [ship]
        await service.list_all()

        mock_repo.find_by_id.return_value = ship
        mock_repo.update.return_value = ship
        await service.update(ship)

        await service.list_all()
        assert mock_repo.find_all.call_count == 2


class TestCacheTTL:
    def test_cache_ttl_is_600(self) -> None:
        assert _CACHE_TTL == 600
