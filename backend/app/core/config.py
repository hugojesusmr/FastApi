from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

load_dotenv()

class Settings(BaseSettings):
    DB_TYPE: str = "sqlite"

    # SQLite
    SQLITE_PATH: str = "./fastapi_app.db"

    # PostgreSQL
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_DB_NAME: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_PORT: int = 5432

    TABLE_NAME: str = "tareas"

    class Config:
        env_file = ".env"
        env_prefix = ''

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "postgres":
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}"
        return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"

settings = Settings()