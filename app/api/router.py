from fastapi import APIRouter
from app.api.uploadfile import upload_router

api_router = APIRouter()

api_router.include_router(upload_router, prefix="/files", tags=["Files"])

