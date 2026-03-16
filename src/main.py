import uvicorn
from fastapi import FastAPI
from hexadian_auth_common.fastapi import JWTAuthDependency, _stub_jwt_auth, register_exception_handlers
from opyoid import Injector

from src.application.ports.inbound.ship_service import ShipService
from src.infrastructure.adapters.inbound.api.ship_router import init_router, router
from src.infrastructure.config.dependencies import AppModule
from src.infrastructure.config.settings import Settings


def create_app() -> FastAPI:
    settings = Settings()
    injector = Injector([AppModule(settings)])

    ship_service = injector.inject(ShipService)
    init_router(ship_service)

    app = FastAPI(title=settings.app_name)

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
    uvicorn.run("src.main:app", host="0.0.0.0", port=8002, reload=True)
