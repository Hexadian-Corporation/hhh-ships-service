from src.domain.models.ship import CargoHold, Ship
from src.infrastructure.adapters.inbound.api.ship_dto import CargoHoldDTO, ShipDTO


class ShipApiMapper:
    @staticmethod
    def to_domain(dto: ShipDTO) -> Ship:
        return Ship(
            id=dto.id,
            name=dto.name,
            manufacturer=dto.manufacturer,
            cargo_holds=[
                CargoHold(name=h.name, volume_scu=h.volume_scu, max_box_size_scu=h.max_box_size_scu)
                for h in dto.cargo_holds
            ],
            total_scu=dto.total_scu,
            scm_speed=dto.scm_speed,
            quantum_speed=dto.quantum_speed,
            landing_time_seconds=dto.landing_time_seconds,
            loading_time_per_scu_seconds=dto.loading_time_per_scu_seconds,
        )

    @staticmethod
    def to_dto(ship: Ship) -> ShipDTO:
        return ShipDTO(
            _id=ship.id,
            name=ship.name,
            manufacturer=ship.manufacturer,
            cargo_holds=[
                CargoHoldDTO(name=h.name, volume_scu=h.volume_scu, max_box_size_scu=h.max_box_size_scu)
                for h in ship.cargo_holds
            ],
            total_scu=ship.total_scu,
            scm_speed=ship.scm_speed,
            quantum_speed=ship.quantum_speed,
            landing_time_seconds=ship.landing_time_seconds,
            loading_time_per_scu_seconds=ship.loading_time_per_scu_seconds,
        )
