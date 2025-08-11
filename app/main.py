# Clase principal que se utiliza para crear una aplicación FastAPI
from fastapi import FastAPI
#  Clase base declarativa para los modelos de SQLAlchemy
from app.db.base import Base
# Este es el motor de SQLAlchemy que se conecta a la base de datos
from app.db.session import engine
# Este es un enrutador que incluye las rutas de la API
from app.routers.router import api_router
from fastapi.staticfiles import StaticFiles
# Este middleware se utiliza para manejar el intercambio de recursos de origen cruzado (CORS), permitiendo que tu API sea accesible desde diferentes orígenes.
from fastapi.middleware.cors import CORSMiddleware

# Inicializa una nueva aplicación en FastAPI.
app = FastAPI()

# Crea todas las tablas definidas en los modelos que heredan de Base en la base de datos. 
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)



