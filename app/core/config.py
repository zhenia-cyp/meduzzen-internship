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

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    REDIS_URL: str
    REDIS_PORT: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_URL}:{self.REDIS_PORT}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()