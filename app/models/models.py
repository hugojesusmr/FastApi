from datetime import datetime
from typing import Dict, Optional, Any
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.mysql import JSON

class ExcelData(SQLModel, table=True):
 
    __tablename__ = "excel_data"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    #Columna JSON para almacenar todos los datos de la fila, el tipo de dato JSON es nativo de MySQL
    data: Dict[str, Any] = Field(sa_column=Column(JSON))
    
    #Campo de referencia para el archivo subido
    file_id: Optional[str] = Field(default=None, index=True)
    
    #Campo para la fecha de carga
    create_at: Optional[datetime] = Field(default=datetime.now())