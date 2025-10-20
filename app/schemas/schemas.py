from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel


# --- Esquema para la creación de datos (petición de la API) ---
class ExcelDateCreate(SQLModel):
    """
    Esquema de entrada modular para crear un registro a través de la API.
    """
    data: Dict[str, Any]

# --- Esquema para la lectura de datos (respuesta d la API) ---
class ExcelDataRead(SQLModel):    
    """
    Esquema de salida modular para leer un registro 
    """
    id: int
    data: Dict[str, Any]
    file_id: Optional[str]

# --- Esquema para conversion de tipos ---
class ColumnTypes(SQLModel):
    """
    Esquema para especificar los tipos de datos de las columnas.
    """    
    data: Dict[str, str]