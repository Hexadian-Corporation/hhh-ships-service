from bson import ObjectId
from pymongo.collection import Collection

from src.application.ports.outbound.ship_repository import ShipRepository
from src.domain.models.ship import Ship
from src.infrastructure.adapters.outbound.persistence.ship_persistence_mapper import ShipPersistenceMapper


class MongoShipRepository(ShipRepository):
    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def save(self, ship: Ship) -> Ship:
        doc = ShipPersistenceMapper.to_document(ship)
        if ship.id:
            self._collection.replace_one({"_id": ObjectId(ship.id)}, doc, upsert=True)
            return ship
        result = self._collection.insert_one(doc)
        ship.id = str(result.inserted_id)
        return ship

    def find_by_id(self, ship_id: str) -> Ship | None:
        doc = self._collection.find_one({"_id": ObjectId(ship_id)})
        if doc is None:
            return None
        return ShipPersistenceMapper.to_domain(doc)

    def find_all(self) -> list[Ship]:
        return [ShipPersistenceMapper.to_domain(doc) for doc in self._collection.find()]

    def delete(self, ship_id: str) -> bool:
        result = self._collection.delete_one({"_id": ObjectId(ship_id)})
        return result.deleted_count > 0
