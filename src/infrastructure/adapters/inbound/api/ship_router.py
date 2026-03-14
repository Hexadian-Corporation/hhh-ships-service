from fastapi import APIRouter, HTTPException

from src.application.ports.inbound.ship_service import ShipService
from src.domain.exceptions.ship_exceptions import ShipNotFoundError
from src.infrastructure.adapters.inbound.api.ship_api_mapper import ShipApiMapper
from src.infrastructure.adapters.inbound.api.ship_dto import ShipDTO

router = APIRouter(prefix="/ships", tags=["ships"])

_ship_service: ShipService | None = None


def init_router(ship_service: ShipService) -> None:
    global _ship_service
    _ship_service = ship_service


@router.post("/", response_model=ShipDTO, status_code=201)
def create_ship(dto: ShipDTO) -> ShipDTO:
    ship = ShipApiMapper.to_domain(dto)
    created = _ship_service.create(ship)
    return ShipApiMapper.to_dto(created)


@router.get("/{ship_id}", response_model=ShipDTO)
def get_ship(ship_id: str) -> ShipDTO:
    try:
        ship = _ship_service.get(ship_id)
    except ShipNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return ShipApiMapper.to_dto(ship)


@router.get("/", response_model=list[ShipDTO])
def list_ships() -> list[ShipDTO]:
    return [ShipApiMapper.to_dto(s) for s in _ship_service.list_all()]


@router.delete("/{ship_id}", status_code=204)
def delete_ship(ship_id: str) -> None:
    try:
        _ship_service.delete(ship_id)
    except ShipNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
