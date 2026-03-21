from unittest.mock import MagicMock, patch

from src.infrastructure.config.dependencies import AppModule
from src.infrastructure.config.settings import Settings


class TestAppModuleClient:
    def test_uses_async_motor_client(self) -> None:
        settings = Settings(mongo_uri="mongodb://localhost:27017", mongo_db="test_db", jwt_secret="test-secret")
        module = AppModule(settings)

        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_db.__getitem__ = MagicMock(return_value=mock_collection)
        mock_client = MagicMock()
        mock_client.__getitem__ = MagicMock(return_value=mock_db)

        with patch("src.infrastructure.config.dependencies.AsyncIOMotorClient", return_value=mock_client) as mock_motor:
            module.configure()

        mock_motor.assert_called_once_with(settings.mongo_uri)

    def test_binds_collection_from_correct_db(self) -> None:
        settings = Settings(mongo_uri="mongodb://localhost:27017", mongo_db="test_db", jwt_secret="test-secret")
        module = AppModule(settings)

        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_db.__getitem__ = MagicMock(return_value=mock_collection)
        mock_client = MagicMock()
        mock_client.__getitem__ = MagicMock(return_value=mock_db)

        with patch("src.infrastructure.config.dependencies.AsyncIOMotorClient", return_value=mock_client):
            module.configure()

        mock_client.__getitem__.assert_called_with(settings.mongo_db)
        mock_db.__getitem__.assert_called_with("ships")
