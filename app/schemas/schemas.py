from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel

# Esquemas de autenticación
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

class TokenData(SQLModel):
    username: Optional[str] = None


# Esquemas de Región
class RegionBase(SQLModel):
    site_code: str
    location_name: str
    service_panda: Optional[str] = None
    city: str
    state: str
    tipo_de_red: str
    region: str
    coordinador: Optional[str] = None
    ingeniero: Optional[str] = None
    km: Optional[float] = None
    ingenieria: Optional[str] = None
    kmz: Optional[str] = None

class RegionCreate(RegionBase):
    pass

class RegionRead(RegionBase):
    id: int
    created_at: Optional[datetime] = None

class RegionUpdate(SQLModel):
    site_code: Optional[str] = None
    location_name: Optional[str] = None
    service_panda: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    tipo_de_red: Optional[str] = None
    region: Optional[str] = None
    coordinador: Optional[str] = None
    ingeniero: Optional[str] = None
    km: Optional[float] = None
    ingenieria: Optional[str] = None
    kmz: Optional[str] = None
