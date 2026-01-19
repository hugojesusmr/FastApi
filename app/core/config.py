from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """ 
    Clase de configuración que carga variables de entorno
    """    
    MYSQL_HOST: str
    MYSQL_DB_NAME: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_PORT: int
    TABLE_NAME: str
 
    class Config:
        env_file = ".env"
        env_prefix = ''

    @property
    def DATABASE_URL(self) -> str:
           return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB_NAME}"

settings = Settings()     