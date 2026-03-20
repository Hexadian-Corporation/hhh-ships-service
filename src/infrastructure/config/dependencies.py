from opyoid import Module, SingletonScope
from pymongo import MongoClient
from pymongo.collation import Collation
from pymongo.collection import Collection

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
        client = MongoClient(self._settings.mongo_uri)
        db = client[self._settings.mongo_db]
        collection = db["ships"]

        collection.create_index("name", collation=Collation(locale="en", strength=2))
        collection.create_index("manufacturer")

        self.bind(Collection, to_instance=collection, scope=SingletonScope)

        mongo_repo = MongoShipRepository(collection)
        self.bind(ShipRepository, to_instance=mongo_repo, scope=SingletonScope)

        ship_service = ShipServiceImpl(
            ship_repository=mongo_repo,
            cache_ttl_seconds=self._settings.cache_ttl_seconds,
            cache_max_size=self._settings.cache_max_size,
        )
        self.bind(ShipService, to_instance=ship_service, scope=SingletonScope)
