from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.application.ports.outbound.ship_repository import ShipRepository
from src.domain.models.ship import Ship
from src.infrastructure.adapters.outbound.persistence.ship_persistence_mapper import ShipPersistenceMapper


class MongoShipRepository(ShipRepository):
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self._collection = collection

    async def save(self, ship: Ship) -> Ship:
        doc = ShipPersistenceMapper.to_document(ship)
        if ship.id:
            await self._collection.replace_one({"_id": ObjectId(ship.id)}, doc, upsert=True)
            return ship
        result = await self._collection.insert_one(doc)
        ship.id = str(result.inserted_id)
        return ship

    async def find_by_id(self, ship_id: str) -> Ship | None:
        doc = await self._collection.find_one({"_id": ObjectId(ship_id)})
        if doc is None:
            return None
        return ShipPersistenceMapper.to_domain(doc)

    async def find_all(self) -> list[Ship]:
        docs = await self._collection.find().to_list(None)
        return [ShipPersistenceMapper.to_domain(doc) for doc in docs]

    async def delete(self, ship_id: str) -> bool:
        result = await self._collection.delete_one({"_id": ObjectId(ship_id)})
        return result.deleted_count > 0

    async def search_by_name(self, query: str) -> list[Ship]:
        docs = await self._collection.find({"name": {"$regex": query, "$options": "i"}}).to_list(None)
        return [ShipPersistenceMapper.to_domain(doc) for doc in docs]

    async def update(self, ship: Ship) -> Ship | None:
        doc = ShipPersistenceMapper.to_document(ship)
        result = await self._collection.replace_one({"_id": ObjectId(ship.id)}, doc)
        if result.matched_count == 0:
            return None
        return ship
