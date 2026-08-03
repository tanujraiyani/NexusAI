from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "NexusAI Gateway"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/nexusai"
    )

    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()