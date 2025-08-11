# Se utiliza para crear una nueva instancia de motor de SQLAlchemy
from sqlalchemy import create_engine 
# Para crear nuevos objetos Session
from sqlalchemy.orm import sessionmaker
# Configuración principal para la conexion a la Base de Datos
from app.core.config import settings

# Esta línea crea un nueva conexión a la base de datos utilizando la cadena de conexión especificada en settings.DATABASE_URL del archivo config.py que esta dentro de la carpeta core
# La opción pool_pre_ping=True verifica si una conexión sigue activa antes de usarla, lo que puede ayudar a evitar problemas con conexiones obsoletas.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
# Creación de sesiones, autocommit y autoflush controlan el comportamiento de la sesión 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función generadora que proporciona una sesión de base de datos
def get_db():
    #  Crea una nueva instancia de sesión
    db = SessionLocal()
    # El bloque try-finally asegura que la sesión se cierre correctamente después de que se complete la solicitud.
    try:
        yield db
    finally:  
        db.close()

