import asyncio
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
        in_game=True,
    ),
    Ship(
        name="Freelancer",
        manufacturer="MISC",
        cargo_holds=[
            CargoHold(name="Main Cargo Hold", volume_scu=66.0),
        ],
        total_scu=66.0,
        scm_speed=195.0,
        quantum_speed=283_046_000.0,
        landing_time_seconds=60.0,
        loading_time_per_scu_seconds=2.0,
        in_game=True,
    ),
    Ship(
        name="Freelancer MAX",
        manufacturer="MISC",
        cargo_holds=[
            CargoHold(name="Main Cargo Hold", volume_scu=120.0),
        ],
        total_scu=120.0,
        scm_speed=180.0,
        quantum_speed=283_046_000.0,
        landing_time_seconds=60.0,
        loading_time_per_scu_seconds=2.5,
        in_game=True,
    ),
    Ship(
        name="Caterpillar",
        manufacturer="Drake",
        cargo_holds=[
            CargoHold(name="Module 1", volume_scu=144.0),
            CargoHold(name="Module 2", volume_scu=144.0),
            CargoHold(name="Module 3", volume_scu=144.0),
            CargoHold(name="Module 4", volume_scu=144.0),
        ],
        total_scu=576.0,
        scm_speed=150.0,
        quantum_speed=283_046_000.0,
        landing_time_seconds=90.0,
        loading_time_per_scu_seconds=3.0,
        in_game=True,
    ),
    Ship(
        name="C2 Hercules",
        manufacturer="Crusader",
        cargo_holds=[
            CargoHold(name="Main Cargo Bay", volume_scu=696.0),
        ],
        total_scu=696.0,
        scm_speed=165.0,
        quantum_speed=283_046_000.0,
        landing_time_seconds=90.0,
        loading_time_per_scu_seconds=3.5,
        in_game=True,
    ),
    Ship(
        name="Hull C",
        manufacturer="MISC",
        cargo_holds=[
            CargoHold(name="External Spindles", volume_scu=4608.0),
        ],
        total_scu=4608.0,
        scm_speed=120.0,
        quantum_speed=283_046_000.0,
        landing_time_seconds=120.0,
        loading_time_per_scu_seconds=4.0,
        in_game=True,
    ),
    Ship(
        name="Cutlass Black",
        manufacturer="Drake",
        cargo_holds=[
            CargoHold(name="Rear Cargo Bay", volume_scu=46.0),
        ],
        total_scu=46.0,
        scm_speed=210.0,
        quantum_speed=283_046_000.0,
        landing_time_seconds=60.0,
        loading_time_per_scu_seconds=1.8,
        in_game=True,
    ),
    Ship(
        name="Constellation Taurus",
        manufacturer="RSI",
        cargo_holds=[
            CargoHold(name="Main Cargo Hold", volume_scu=168.0),
        ],
        total_scu=168.0,
        scm_speed=175.0,
        quantum_speed=283_046_000.0,
        landing_time_seconds=60.0,
        loading_time_per_scu_seconds=2.8,
        in_game=True,
    ),
]


async def seed_ships(service: ShipService) -> list[Ship]:
    """Seed ships if none exist. Idempotent."""
    existing = await service.list_all()
    if existing:
        return []

    copies = [replace(ship_data, cargo_holds=[replace(h) for h in ship_data.cargo_holds]) for ship_data in SHIPS]
    return list(await asyncio.gather(*[service.create(ship) for ship in copies]))
