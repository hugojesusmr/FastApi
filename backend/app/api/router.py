from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.pdf import router as pdf_router

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(pdf_router)

