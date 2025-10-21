from sqlmodel import select
from typing import List, Optional
from sqlalchemy.asyncio import AsyncSession
from app.models.models import Tareas
from app.schemas.schemas import TareaCreate, TareaUpdate

async def create_tarea(db: AsyncSession, tara_in: TareaCreate) -> Tareas:
    db_incidence = Incidence(**incidence.dict())
    db.add(db_incidence)
    db.commit()
    db.refresh(db_incidence)
    return db_incidence
