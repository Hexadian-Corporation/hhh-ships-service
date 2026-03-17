from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from hexadian_auth_common.fastapi import require_permission

from src.application.ports.inbound.ship_service import ShipService
from src.domain.exceptions.ship_exceptions import ShipNotFoundError
from src.infrastructure.adapters.inbound.api.ship_api_mapper import ShipApiMapper
from src.infrastructure.adapters.inbound.api.ship_dto import ShipDTO

router = APIRouter(prefix="/ships", tags=["ships"])

_ship_service: ShipService | None = None

_read = [Depends(require_permission("hhh:ships:read"))]
_write = [Depends(require_permission("hhh:ships:write"))]
_delete = [Depends(require_permission("hhh:ships:delete"))]

_CACHE_MAX_AGE = 900


def init_router(ship_service: ShipService) -> None:
    global _ship_service
    _ship_service = ship_service


@router.post("/", response_model=ShipDTO, status_code=201, dependencies=_write)
def create_ship(dto: ShipDTO) -> ShipDTO:
    ship = ShipApiMapper.to_domain(dto)
    created = _ship_service.create(ship)
    return ShipApiMapper.to_dto(created)


@router.get("/{ship_id}", response_model=ShipDTO, dependencies=_read)
def get_ship(ship_id: str) -> JSONResponse:
    try:
        ship = _ship_service.get(ship_id)
    except ShipNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    dto = ShipApiMapper.to_dto(ship)
    return JSONResponse(
        content=dto.model_dump(by_alias=True),
        headers={"Cache-Control": f"max-age={_CACHE_MAX_AGE}"},
    )


@router.get("/", response_model=list[ShipDTO], dependencies=_read)
def list_ships() -> JSONResponse:
    dtos = [ShipApiMapper.to_dto(s) for s in _ship_service.list_all()]
    return JSONResponse(
        content=[d.model_dump(by_alias=True) for d in dtos],
        headers={"Cache-Control": f"max-age={_CACHE_MAX_AGE}"},
    )


@router.delete("/{ship_id}", status_code=204, dependencies=_delete)
def delete_ship(ship_id: str) -> None:
    try:
        _ship_service.delete(ship_id)
    except ShipNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
