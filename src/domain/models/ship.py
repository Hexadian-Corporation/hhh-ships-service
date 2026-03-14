from dataclasses import dataclass, field


@dataclass
class CargoHold:
    """A cargo hold within a ship."""

    name: str
    volume_scu: float
    max_box_size_scu: float


@dataclass
class Ship:
    """Domain model representing a ship and its capabilities."""

    id: str | None = None
    name: str = ""
    manufacturer: str = ""
    cargo_holds: list[CargoHold] = field(default_factory=list)
    total_scu: float = 0.0
    scm_speed: float = 0.0
    quantum_speed: float = 0.0
    landing_time_seconds: float = 0.0
    loading_time_per_scu_seconds: float = 0.0
