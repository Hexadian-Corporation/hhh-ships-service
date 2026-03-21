from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from opyoid import Module, SingletonScope

from src.application.ports.inbound.ship_service import ShipService
from src.application.ports.outbound.ship_repository import ShipRepository
from src.application.services.ship_service_impl import ShipServiceImpl
from src.infrastructure.adapters.outbound.persistence.mongo_ship_repository import MongoShipRepository
from src.infrastructure.config.settings import Settings


class AppModule(Module):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self._settings = settings

    def configure(self) -> None:
        client = AsyncIOMotorClient(self._settings.mongo_uri)
        db = client[self._settings.mongo_db]
        collection = db["ships"]

        self.bind(AsyncIOMotorCollection, to_instance=collection, scope=SingletonScope)

        mongo_repo = MongoShipRepository(collection)
        self.bind(ShipRepository, to_instance=mongo_repo, scope=SingletonScope)

        ship_service = ShipServiceImpl(
            ship_repository=mongo_repo,
            cache_ttl_seconds=self._settings.cache_ttl_seconds,
            cache_max_size=self._settings.cache_max_size,
        )
        self.bind(ShipService, to_instance=ship_service, scope=SingletonScope)
