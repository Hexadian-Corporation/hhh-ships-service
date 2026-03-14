from abc import ABC, abstractmethod

from src.domain.models.ship import Ship


class ShipService(ABC):
    @abstractmethod
    def create_ship(self, ship: Ship) -> Ship: ...

    @abstractmethod
    def get_ship(self, ship_id: str) -> Ship | None: ...

    @abstractmethod
    def list_ships(self) -> list[Ship]: ...

    @abstractmethod
    def delete_ship(self, ship_id: str) -> bool: ...
