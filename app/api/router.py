<<<<<<< HEAD
from fastapi import APIRouter
from app.api.tareas import upload_router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["ML Dashboard"])
api_router.include_router(upload_router, prefix="/tareas", tags=["Tareas - Importación y Transformación"])

=======
from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.regions import router as regions_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(regions_router, prefix="/regions", tags=["Regiones"])

>>>>>>> 8150643 (update)
