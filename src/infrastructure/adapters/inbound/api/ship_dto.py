from pydantic import BaseModel, Field


class CargoHoldDTO(BaseModel):
    name: str
    volume_scu: float
    max_box_size_scu: float


class ShipDTO(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    name: str
    manufacturer: str
    cargo_holds: list[CargoHoldDTO] = Field(default_factory=list)
    total_scu: float = 0.0
    scm_speed: float = 0.0
    quantum_speed: float = 0.0
    landing_time_seconds: float = 0.0
    loading_time_per_scu_seconds: float = 0.0

    model_config = {"populate_by_name": True}
