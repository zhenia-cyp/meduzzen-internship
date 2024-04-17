from typing import ClassVar
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Environment settings for the application.
    """
    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))

    REDIS_URL: str = os.getenv("REDIS_URL", "")
    REDIS_PORT: str = os.getenv("REDIS_PORT", "")

    DATABASE_URL: ClassVar[
        str] = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        model_config = {
            'ignored_types': [
                'DATABASE_URL',
            ]
        }

settings = Settings()