from unittest.mock import MagicMock, call, patch

from pymongo.collation import Collation

from src.infrastructure.config.dependencies import AppModule
from src.infrastructure.config.settings import Settings


class TestAppModuleIndexes:
    def test_creates_name_index_with_collation(self) -> None:
        settings = Settings(mongo_uri="mongodb://localhost:27017", mongo_db="test_db", jwt_secret="test-secret")
        module = AppModule(settings)

        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_db.__getitem__ = MagicMock(return_value=mock_collection)
        mock_client = MagicMock()
        mock_client.__getitem__ = MagicMock(return_value=mock_db)

        with patch("src.infrastructure.config.dependencies.MongoClient", return_value=mock_client):
            module.configure()

        calls = mock_collection.create_index.call_args_list
        assert len(calls) == 2

        name_call = calls[0]
        assert name_call == call("name", collation=Collation(locale="en", strength=2))

    def test_creates_manufacturer_index(self) -> None:
        settings = Settings(mongo_uri="mongodb://localhost:27017", mongo_db="test_db", jwt_secret="test-secret")
        module = AppModule(settings)

        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_db.__getitem__ = MagicMock(return_value=mock_collection)
        mock_client = MagicMock()
        mock_client.__getitem__ = MagicMock(return_value=mock_db)

        with patch("src.infrastructure.config.dependencies.MongoClient", return_value=mock_client):
            module.configure()

        calls = mock_collection.create_index.call_args_list
        manufacturer_call = calls[1]
        assert manufacturer_call == call("manufacturer")
