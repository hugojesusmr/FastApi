from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.core.auth import get_current_active_user
from app.core.ml_analytics import MLAnalyticsService
from app.schemas.schemas import MLDashboardResponse
from app.models.models import User

router = APIRouter()

@router.get("/data", response_model=MLDashboardResponse)
async def get_dashboard_data(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """API endpoint para obtener datos del dashboard"""
    return await MLAnalyticsService.get_dashboard_data(session)

