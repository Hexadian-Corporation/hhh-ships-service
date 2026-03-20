from abc import ABC, abstractmethod

from src.domain.models.ship import Ship


class ShipService(ABC):
    @abstractmethod
    def create(self, ship: Ship) -> Ship: ...

    @abstractmethod
    def get(self, ship_id: str) -> Ship: ...

    @abstractmethod
    def list_all(self) -> list[Ship]: ...

    @abstractmethod
    def delete(self, ship_id: str) -> None: ...

    @abstractmethod
    def search_by_name(self, query: str) -> list[Ship]: ...

    @abstractmethod
    def update(self, ship: Ship) -> Ship: ...
