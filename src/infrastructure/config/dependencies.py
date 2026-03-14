from opyoid import Module, SingletonScope
from pymongo import MongoClient
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

        self.bind(Collection, to_instance=collection, scope=SingletonScope)
        self.bind(ShipRepository, to_class=MongoShipRepository, scope=SingletonScope)
        self.bind(ShipService, to_class=ShipServiceImpl, scope=SingletonScope)
