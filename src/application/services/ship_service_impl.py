from cachetools import TTLCache

from src.application.ports.inbound.ship_service import ShipService
from src.application.ports.outbound.ship_repository import ShipRepository
from src.domain.exceptions.ship_exceptions import ShipNotFoundError
from src.domain.models.ship import Ship

_CACHE_MAXSIZE = 128
_CACHE_TTL = 600
_LIST_CACHE_KEY = "list:all"
_SHIP_KEY_PREFIX = "ship:"
_SEARCH_KEY_PREFIX = "search:"


class ShipServiceImpl(ShipService):
    def __init__(self, ship_repository: ShipRepository) -> None:
        self._repository = ship_repository
        self._cache: TTLCache[str, Ship | list[Ship]] = TTLCache(maxsize=_CACHE_MAXSIZE, ttl=_CACHE_TTL)

    def create_ship(self, ship: Ship) -> Ship:
        result = self._repository.save(ship)
        self._cache.clear()
        return result

    def get_ship(self, ship_id: str) -> Ship | None:
        key = f"{_SHIP_KEY_PREFIX}{ship_id}"
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        ship_found = self._repository.find_by_id(ship_id)
        if ship_found is not None:
            self._cache[key] = ship_found
        return ship_found

    def list_ships(self) -> list[Ship]:
        cached = self._cache.get(_LIST_CACHE_KEY)
        if cached is not None:
            return cached
        ships = self._repository.find_all()
        self._cache[_LIST_CACHE_KEY] = ships
        return ships

    def delete_ship(self, ship_id: str) -> bool:
        result = self._repository.delete(ship_id)
        self._cache.clear()
        return result

    def search_by_name(self, query: str) -> list[Ship]:
        if not query.strip():
            return []
        key = f"{_SEARCH_KEY_PREFIX}{query.lower()}"
        cached = self._cache.get(key)
        if cached is not None:
            return cached  # type: ignore[return-value]
        results = self._repository.search_by_name(query)
        self._cache[key] = results
        return results

    def update_ship(self, ship: Ship) -> Ship:
        existing = self._repository.find_by_id(ship.id)
        if existing is None:
            raise ShipNotFoundError(ship.id)
        result = self._repository.update(ship)
        if result is None:
            raise ShipNotFoundError(ship.id)
        self._cache.clear()
        return result
