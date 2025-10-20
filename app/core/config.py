from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """ 
    Configuración de la aplicación cargada desde variables de entorno
    """    
    DATABASE_URL: str 
 
    class Config:
        env_file = ".env"

settings = Settings()     