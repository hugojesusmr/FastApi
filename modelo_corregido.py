from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Tareas(SQLModel, table=True):
    __tablename__ = "tareas"
    
    tarea: str = Field(primary_key=True)
    grupo_de_asignacion: Optional[str] = None
    plataforma: Optional[str] = None
    nombre_de_tarea: Optional[str] = None
    prioridad: Optional[str] = None
    incidente: Optional[str] = None
    estado: Optional[str] = None
    fecha_de_creacion: Optional[datetime] = None
    fin_de_semana: Optional[str] = None
    viernes_fuera_de_horario_laboral: Optional[str] = None
    mes: Optional[str] = None
    semana: Optional[str] = None
    trimestre: Optional[str] = None
    tipo_de_solicitud: Optional[str] = None
    motivo_del_estado: Optional[str] = None
    fechas_solicitud_almacen: Optional[datetime] = None
    fecha_liberacion_almacen: Optional[datetime] = None
    fecha_entrega_en_sitio: Optional[datetime] = None
    fecha_solicitud_a_proveedor: Optional[datetime] = None
    fecha_de_envio_del_proveedor: Optional[datetime] = None
    fecha_entrega_en_sitio_spms: Optional[datetime] = None
    tipo_de_transporte: Optional[str] = None
    asignado_a: Optional[str] = None
    region_operativa: Optional[str] = None
    motivo_fuera_de_sla: Optional[str] = None