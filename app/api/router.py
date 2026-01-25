from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.regions import router as regions_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(regions_router, prefix="/regions", tags=["Regiones"])

