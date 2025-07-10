from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncidenceCreate(BaseModel):
    number: str = None
    inicio_de_falla : Optional[datetime] = None
    fecha_de_envio: Optional[datetime] = None
    fecha_resolucion_falla: Optional[datetime] = None
    priority: Optional[int] = None
    actual_assignment_group: Optional[str] = None
    state: Optional[str] = None
    resolution_code_n1: Optional[str] = None
    resolution_code_n2: Optional[str] = None
    resolution_code_n3: Optional[str] = None
    resolution_notes: Optional[str] = None
    afectacion_al_servicio: Optional[str] = None
    category_ci: Optional[str] = None
    cmdb_ci: Optional[str] = None



