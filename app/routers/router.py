from fastapi import APIRouter
from app.routers.incidence_router import upload_router
from app.routers.item_router import item_router

api_router = APIRouter()

api_router.include_router(upload_router, prefix="/files", tags=["Files"])
api_router.include_router(item_router, prefix="/items", tags=["Items"])

