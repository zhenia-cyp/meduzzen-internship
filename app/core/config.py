from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Environment settings for the application.
    """
    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = os.getenv("PORT", 8000)
    DEBUG: bool = os.getenv("DEBUG", True)
    RELOAD: bool = os.getenv("RELOAD", True)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()