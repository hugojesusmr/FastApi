from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base

class Incidence(Base):
    __tablename__ = "incidences"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number = Column(String(50), unique=True, index=True, nullable=True)
    inicio_de_falla = Column(String(50), nullable=True)
    fecha_de_envio = Column(String(50), nullable=True)
    fecha_resolucion_falla = Column(String(50), nullable=True)
    priority = Column(Integer, nullable=True)
    actual_assignment_group = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)
    resolution_code_n1 = Column(String(50), nullable=True)
    resolution_code_n2 = Column(String(50), nullable=True)
    resolution_code_n3 = Column(String(50), nullable=True)
    resolution_notes = Column(String(255), nullable=True)
    afectacion_al_servicio = Column(String(50), nullable=True)
    category_ci = Column(String(100), nullable=True)
    cmdb_ci = Column(String(100), nullable=True)



    
