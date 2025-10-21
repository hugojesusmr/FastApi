import io
import uuid
import time
import numpy as np
import pandas as pd
from io import BytesIO
from sqlalchemy import select
from datetime import date, datetime
from typing import Optional, Dict, Any
from app.db.session import get_session
from app.models.models import ExcelData
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import ColumnTypes, ExcelDataRead, ExcelDateCreate
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends

upload_router = APIRouter()
temp_dfs = {}

def _get_sql_dtype(pd_type: str) -> str:
    if pd.api.types.is_integer_dtype(pd_type):
        return 'BIGINT'
    elif pd.api.types.is_float_dtype(pd_type):
        return 'DOUBLE'
    elif pd.api.types.is_datetime64_any_dtype(pd_type):
        return 'DATETIME'
    elif pd.api.types.is_timedelta64_dtype(pd_type):
        return 'VARCHAR(255)'
    else:
        return 'TEXT'

def _format_value_for_sql(value):
    if pd.isnull(value):
        return 'NULL'
    if isinstance(value, (pd.Timestamp, datetime, date)):
        return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
    if isinstance(value, str):
        return f"'{value.replace("'", "''")}'"  # Escapa comillas simples
    return str(value)

@upload_router.get("/")
def read_root():
    return {"message":"Bienvenido a la API de Conversión de Excel"}


@upload_router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    """
    Recibe un archivo Excel, lo lee y devuelve los nombres de las columnas
    """
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Archivo no Valido")
    
    try:
        contents = await file.read()
        excel_file = BytesIO(contents)
        df = pd.read_excel(excel_file, engine="openpyxl")
        
        # 1. Busca columnas que probablemente sean fechas
        fecha_columnas = [col for col in df.columns if 'fecha' in col.lower() or 'date' in col.lower()]

        # 2. Convierte columnas numéricas (int64/float64) a fecha usando el origen de Excel
        for col in fecha_columnas:
            if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = pd.to_datetime(df[col], unit='D', origin='1899-12-30', errors='coerce')

        # 3. (Opcional) Si tienes columnas de fecha en texto, también puedes convertirlas aquí
        for col in fecha_columnas:
            if pd.api.types.is_object_dtype(df[col]):
                df[col] = pd.to_datetime(df[col], errors='coerce')

        file_id = str(uuid.uuid4())
        temp_dfs[file_id] = df
        columns_names = list(df.columns)
        # Opcional: puedes devolver también los tipos detectados
        columns_types = [str(df[col].dtype) for col in df.columns]

        return {"file_id": file_id, "columns": columns_names, "types": columns_types}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error al procesar el archivo: {e}"
        )


@upload_router.get("download_sql/{file_id}", response_class=StreamingResponse)
async def download_sql_file(file_id: str):
    if file_id not in temp_dfs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Archivo no Encontrado")
    
    df = temp_dfs[file_id]
    buffer = io.StringIO()
    table_name = "historico" 

    columns = []

    for col_name, pd_type in df.dtypes.items():
        sql_type = _get_sql_dtype(str(pd_type))
        columns.append(f"'{col_name}' '{sql_type}'")

    create_table_sql = f"CREATE TABLE '{table_name}' (\n"
    create_table_sql += ",\n".join([f"{c}" for c in columns])
    create_table_sql += "\n);\n\n"
    buffer.write(create_table_sql)

    columns_list = ", ".join([f"{col}" for col in df.columns])
    batch_size = 1000

    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i+batch_size]

        values_list = []
        for _, row in batch_df.iterrows():
            values = [_format_value_for_sql(row[col]) for col in batch_df.columns]
            values_list.append(f"({', '.join(values)})")
        
        sql_insert = f"INSERT INTO '{table_name}'({columns_list}) VALUES \n"
        sql_insert += ",\n".join(values_list)
        sql_insert += ";\n"
        buffer.write(sql_insert)
    buffer.seek(0)

    return StreamingResponse(
        content=(line for line in buffer),
        media_type="application/sql",
        headers={"Content-Disposition": f"attachment; filename={table_name}.sql"}
    )    

@upload_router.post("/insert_data/")
async def insert_data(file_id: str, session: AsyncSession = Depends(get_session)):
    if file_id not in temp_dfs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Archivo no Encontrado.")

    df = temp_dfs.pop(file_id)

    for col in df.select_dtypes(include=['datetime64[ns]']).columns:
        df[col] = df[col].astype(str)
    
    all_data = df.to_dict('records')
    records_save = [ExcelData(data=row_dict, file_id=file_id) for row_dict in all_data]
    try:
        session.add_all(records_save)
        return {"message": f"{len(records_save)} registros insertados con éxito"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al insertar datos: {e}")    


