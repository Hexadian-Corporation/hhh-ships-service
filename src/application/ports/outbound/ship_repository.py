from abc import ABC, abstractmethod

from src.domain.models.ship import Ship


class ShipRepository(ABC):
    @abstractmethod
    def save(self, ship: Ship) -> Ship: ...

    @abstractmethod
    def find_by_id(self, ship_id: str) -> Ship | None: ...

    @abstractmethod
    def find_all(self) -> list[Ship]: ...

    @abstractmethod
    def delete(self, ship_id: str) -> bool: ...

    @abstractmethod
    def search_by_name(self, query: str) -> list[Ship]: ...

    @abstractmethod
    def update(self, ship: Ship) -> Ship | None: ...
