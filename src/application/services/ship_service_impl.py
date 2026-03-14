from src.application.ports.inbound.ship_service import ShipService
from src.application.ports.outbound.ship_repository import ShipRepository
from src.domain.models.ship import Ship


class ShipServiceImpl(ShipService):

    def __init__(self, ship_repository: ShipRepository) -> None:
        self._repository = ship_repository

    def create_ship(self, ship: Ship) -> Ship:
        return self._repository.save(ship)

    def get_ship(self, ship_id: str) -> Ship | None:
        return self._repository.find_by_id(ship_id)

    def list_ships(self) -> list[Ship]:
        return self._repository.find_all()

    def delete_ship(self, ship_id: str) -> bool:
        return self._repository.delete(ship_id)
