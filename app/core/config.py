from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Environment settings for the application.
    """
    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"