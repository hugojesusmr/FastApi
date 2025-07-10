import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "FastAPI conecction witn MySQL"
    PROJECT_VERSION: str = "1.0.0"

    MYSQL_USER : str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT")
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DATABASE}"

settings = Settings()     