from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.services.pdf import PdfService
from app.schemas.pdf import PdfExtractResponse, RegionRequest, RegionExtractResponse
from app.core.auth import get_current_active_user
from app.models.user import User
import json

router = APIRouter(prefix="/pdf", tags=["pdf"])

@router.post("/extract", response_model=PdfExtractResponse)
async def extract_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    service = PdfService()
    return await service.extract_text(file)

@router.post("/extract-region", response_model=RegionExtractResponse)
async def extract_region(
    file: UploadFile = File(...),
    region: str = Form(...),
    current_user: User = Depends(get_current_active_user)
):
    region_data = RegionRequest(**json.loads(region))
    service = PdfService()
    return await service.extract_region(file, region_data)
