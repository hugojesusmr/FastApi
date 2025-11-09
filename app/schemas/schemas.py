from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class TareaBase(SQLModel):
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
    tiempo_1: Optional[float] = None
    etapa_1: Optional[str] = None
    horas_1: Optional[float] = None
    hrs_1: Optional[str] = None
    dias_1: Optional[str] = None
    sla_no: Optional[str] = None
    tiempo_2: Optional[float] = None
    etapa_2: Optional[str] = None
    horas_2: Optional[float] = None
    hrs_2: Optional[str] = None
    dias_2: Optional[str] = None
    sla_almacen: Optional[str] = None
    tiempo_3: Optional[float] = None
    etapa_3: Optional[str] = None
    horas_3: Optional[float] = None
    hrs_3: Optional[str] = None
    dias_3: Optional[str] = None
    sla_trafico: Optional[str] = None
    es_top_10: Optional[str] = None
    status_calculo: Optional[str] = None

class TareaCreate(TareaBase):
    id_tarea: str

class TareaRead(TareaBase):
    id_tarea: str

class TareaUpdate(TareaBase):
    id_tarea: Optional[str] = None

class UserBase(SQLModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

class UserLogin(SQLModel):
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str
