from abc import ABC, abstractmethod

from src.domain.models.ship import Ship


class ShipService(ABC):
    @abstractmethod
    async def create(self, ship: Ship) -> Ship: ...

    @abstractmethod
    async def get(self, ship_id: str) -> Ship: ...

    @abstractmethod
    async def list_all(self) -> list[Ship]: ...

    @abstractmethod
    async def delete(self, ship_id: str) -> None: ...

    @abstractmethod
    async def search_by_name(self, query: str) -> list[Ship]: ...

    @abstractmethod
    async def update(self, ship: Ship) -> Ship: ...
