import os

from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"

    class Config:
        env_file = os.path.join(BASE_DIR.parent, ".env")
        env_file_encoding = "utf-8"


settings = Settings()
