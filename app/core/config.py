from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """ 
    Clase de configuración que carga variables de entorno
    """    
    POSTGRES_HOST: str
    POSTGRES_DB_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    TABLE_NAME: str = "tareas"
 
    class Config:
        env_file = ".env"
        env_prefix = ''

    @property
    def DATABASE_URL(self) -> str:
           return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}"

settings = Settings()     