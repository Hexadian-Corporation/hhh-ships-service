from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "hhh-ships-service"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "hhh_ships"
    host: str = "0.0.0.0"
    port: int = 8002
    jwt_secret: str
    jwt_algorithm: str = "HS256"

    model_config = {"env_prefix": "HHH_SHIPS_"}
