import polars as pl
from io import BytesIO
from datetime import datetime
from app.db.session import get_session
from app.schemas.schemas import TareaCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.polars_transform import apply_transformations
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends

upload_router = APIRouter()

@upload_router.post("/upload", summary="Sube, Transforma y Guarda")
async def Upload_tareas_file(file: UploadFile = File(..., description="Archivo CSV o Excel con Datos"),db: AsyncSession = Depends(get_session)):
    """
    Sube un archivo, aplica transformaciones y Guarda los resultados en la base de datos de forma asíncrona
    """

    # 1. --- Lectura del Archivo ---
    content_type = file.content_type
    content = await file.read()

    try:
        if content_type == 'text/csv':
            df_initial = pl.read_csv(BytesIO(content), try_parse_dates=True)
        elif content_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:    
            df_initial = pl.read_excel(BytesIO(content), engine='openpyxl')
        else:
            raise ValueError("Tipo de archivo no soportado")     
    except Exception as e:    
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al leer el archivo: {e}")


    # 2. --- Aplicar Transformaciones ---
    try:
        df_transformed = apply_transformations(df_initial) 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la transofmración de Polars: {e}")   
    
    #3. --- Inserción de datos ----

    data_to_insert = df_transformed.to_dicts()

    imported_count = 0
    errors = []

    for index, tarea_data in enumerate(data_to_insert):
        try:
            # Validar y Crear el objeto Pydantic/SQLModel
            tarea_in = TareaCreate(**tarea_data)

            await create_tarea(db=db, tarea_in=tarea_in)
            imported_count += 1
        except Exception as e:
            tarea_id = tarea_data.get('Tarea', 'N/A')
            errors.append(f"Fila {index + 2} (Tarea: {tarea_id}): Error al Insertar en DB/validación - {e}")    

    if errors:
        return{
            "message": f"Se importaron {imported_count} tareas, pero {len(errors)} tivieron errores de DB/validación,",
            "status_code": status.HTTP_207_MULTI_STATUS,
            "errors": errors
        }        

    return {
        "message": f"Archivo Procesado y Transformado con éxito. Se importaron {imported_count} tareas."
    }    