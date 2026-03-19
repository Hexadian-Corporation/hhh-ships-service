from dataclasses import replace

from src.domain.models.ship import CargoHold, Ship
from src.infrastructure.adapters.inbound.api.ship_dto import CargoHoldDTO, ShipDTO, ShipUpdateDTO


class ShipApiMapper:
    @staticmethod
    def to_domain(dto: ShipDTO) -> Ship:
        return Ship(
            id=dto.id,
            name=dto.name,
            manufacturer=dto.manufacturer,
            cargo_holds=[CargoHold(name=h.name, volume_scu=h.volume_scu) for h in dto.cargo_holds],
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
            cargo_holds=[CargoHoldDTO(name=h.name, volume_scu=h.volume_scu) for h in ship.cargo_holds],
            total_scu=ship.total_scu,
            scm_speed=ship.scm_speed,
            quantum_speed=ship.quantum_speed,
            landing_time_seconds=ship.landing_time_seconds,
            loading_time_per_scu_seconds=ship.loading_time_per_scu_seconds,
        )

    @staticmethod
    def update_to_domain(existing: Ship, dto: ShipUpdateDTO) -> Ship:
        updates: dict = {}
        if dto.name is not None:
            updates["name"] = dto.name
        if dto.manufacturer is not None:
            updates["manufacturer"] = dto.manufacturer
        if dto.cargo_holds is not None:
            updates["cargo_holds"] = [CargoHold(name=h.name, volume_scu=h.volume_scu) for h in dto.cargo_holds]
        if dto.total_scu is not None:
            updates["total_scu"] = dto.total_scu
        if dto.scm_speed is not None:
            updates["scm_speed"] = dto.scm_speed
        if dto.quantum_speed is not None:
            updates["quantum_speed"] = dto.quantum_speed
        if dto.landing_time_seconds is not None:
            updates["landing_time_seconds"] = dto.landing_time_seconds
        if dto.loading_time_per_scu_seconds is not None:
            updates["loading_time_per_scu_seconds"] = dto.loading_time_per_scu_seconds
        return replace(existing, **updates) if updates else existing
