import os
from functools import lru_cache
from typing import Optional
# New import - use this instead
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    APP_NAME: str = "Task Management API"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    TEST_DATABASE_URL: Optional[str] = None

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    class Config:
        case_sensitive = True
        env_file = "../.env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
