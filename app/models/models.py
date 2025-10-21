from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Tareas(SQLModel, table=True):
    __tablename__ = "tareas"
    
    Tarea: str = Field(primary_key=True)
    Grupo_de_asignación: Optional[str] = None
    Plataforma: Optional[str] = None
    Nombre_de_tarea: Optional[str] = None
    Prioridad: Optional[str] = None
    Incidente: Optional[str] = None
    Estado: Optional[str] = None
    Fecha_de_creación: Optional[datetime] = None
    Fin_de_semana: Optional[str] = None
    Viernes_fuera_de_Horario_laboral: Optional[str] = None
    Mes: Optional[str] = None
    Semana: Optional[str] = None
    Trimestre: Optional[str] = None
    Tipo_de_solicitud: Optional[str] = None
    Motivo_del_estado: Optional[str] = None
    Fechas_solicitud_almacén: Optional[datetime] = None
    Fecha_liberación_almacén: Optional[datetime] = None
    Fecha_entrega_en_sitio: Optional[datetime] = None
    Fecha_solicitud_a_proveedor: Optional[datetime] = None
    Fecha_de_envío_del_proveedor: Optional[datetime] = None
    Fecha_entrega_en_sitio_SPMS: Optional[datetime] = None
    Tipo_de_Transporte: Optional[str] = None
    Asignado_a: Optional[str] = None
    Región_Operativa: Optional[str] = None
    Motivo_Fuera_de_SLA: Optional[str] = None
