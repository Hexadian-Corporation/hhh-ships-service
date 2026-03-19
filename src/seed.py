from dataclasses import replace

from src.application.ports.inbound.ship_service import ShipService
from src.domain.models.ship import CargoHold, Ship

SHIPS = [
    Ship(
        name="Zeus MK-2 CL",
        manufacturer="RSI",
        cargo_holds=[
            CargoHold(name="Main Hold", volume_scu=96.0),
            CargoHold(name="Secondary Hold", volume_scu=32.0),
        ],
        total_scu=128.0,
        scm_speed=210.0,
        quantum_speed=283_046_000.0,
        landing_time_seconds=120.0,
        loading_time_per_scu_seconds=3.0,
    ),
]


def seed_ships(service: ShipService) -> list[Ship]:
    """Seed ships if none exist. Idempotent."""
    existing = service.list_all()
    if existing:
        return []

    created = []
    for ship_data in SHIPS:
        ship = replace(ship_data)
        created.append(service.create(ship))
    return created
