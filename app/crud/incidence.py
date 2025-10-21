from sqlalchemy.orm import Session
from app.models.incidence import Incidence
from app.schemas.incidence import IncidenceCreate

async def create_incidence(db: Session, incidence: IncidenceCreate):
    db_incidence = Incidence(**incidence.dict())
    db.add(db_incidence)
    db.commit()
    db.refresh(db_incidence)
    return db_incidence
