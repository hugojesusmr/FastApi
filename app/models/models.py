
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Region(SQLModel, table=True):
    __tablename__ = "regions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    site_code: str = Field(index=True)
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