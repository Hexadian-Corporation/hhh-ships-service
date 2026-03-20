from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "hhh-ships-service"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "hhh_ships"
    host: str = "0.0.0.0"
    port: int = 8002
    jwt_secret: str = Field(default="change-me-in-production", validation_alias="HEXADIAN_AUTH_JWT_SECRET")
    jwt_algorithm: str = "HS256"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000", "http://localhost:3001"])
    cache_ttl_seconds: int = 600
    cache_max_size: int = 128

    model_config = {"env_prefix": "HHH_SHIPS_", "populate_by_name": True}
