from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hexadian_auth_common.fastapi import JWTAuthDependency, _stub_jwt_auth, register_exception_handlers
from motor.motor_asyncio import AsyncIOMotorCollection
from opyoid import Injector
from pymongo.collation import Collation

from src.application.ports.inbound.ship_service import ShipService
from src.infrastructure.adapters.inbound.api.ship_router import init_router, router
from src.infrastructure.config.dependencies import AppModule
from src.infrastructure.config.settings import Settings
from src.seed import seed_ships


def create_app() -> FastAPI:
    settings = Settings()
    injector = Injector([AppModule(settings)])

    ship_service = injector.inject(ShipService)
    init_router(ship_service)

    collection = injector.inject(AsyncIOMotorCollection)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        await collection.create_index("name", collation=Collation(locale="en", strength=2))
        await collection.create_index("manufacturer")
        await seed_ships(ship_service)
        yield

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    jwt_auth = JWTAuthDependency(secret=settings.jwt_secret, algorithm=settings.jwt_algorithm)
    app.dependency_overrides[_stub_jwt_auth] = jwt_auth
    register_exception_handlers(app)

    app.include_router(router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "service": settings.app_name}

    return app


app = create_app()

if __name__ == "__main__":
    _settings = Settings()
    uvicorn.run("src.main:app", host=_settings.host, port=_settings.port, reload=True)
