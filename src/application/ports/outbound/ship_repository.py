from abc import ABC, abstractmethod

from src.domain.models.ship import Ship


class ShipRepository(ABC):
    @abstractmethod
    async def save(self, ship: Ship) -> Ship: ...

    @abstractmethod
    async def find_by_id(self, ship_id: str) -> Ship | None: ...

    @abstractmethod
    async def find_all(self) -> list[Ship]: ...

    @abstractmethod
    async def delete(self, ship_id: str) -> bool: ...

    @abstractmethod
    async def search_by_name(self, query: str) -> list[Ship]: ...

    @abstractmethod
    async def update(self, ship: Ship) -> Ship | None: ...
