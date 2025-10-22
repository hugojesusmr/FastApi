from sqlmodel import select
from typing import List, Optional
from app.models.models import Tareas
from sqlalchemy.asyncio import AsyncSession
from app.schemas.schemas import TareaCreate, TareaUpdate

async def create_tarea(db: AsyncSession, tara_in: TareaCreate) -> Tareas:
    db_tarea = Tareas(**tareas_in.model_dump())
    db.add(db_tarea)
    db.refresh(db_tarea)
    return db_tarea 
