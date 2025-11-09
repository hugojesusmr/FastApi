from sqlmodel import select
from typing import List, Optional
from app.models.models import Tareas
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import TareaCreate, TareaUpdate

async def create_tarea(db: AsyncSession, tarea_in: TareaCreate) -> Tareas:
    try:
        db_tarea = Tareas(**tarea_in.dict())
        db.add(db_tarea)
        await db.commit()
        await db.refresh(db_tarea)
        return db_tarea
    except Exception as e:
        await db.rollback()
        raise e

async def create_tareas_bulk(db: AsyncSession, tareas_data: list) -> int:
    try:
        db_tareas = [Tareas(**data) for data in tareas_data]
        db.add_all(db_tareas)
        await db.commit()
        return len(db_tareas)
    except Exception as e:
        await db.rollback()
        raise e 
