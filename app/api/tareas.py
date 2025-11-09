import pandas as pd
from io import BytesIO
from datetime import datetime
from app.db.session import get_session
from app.schemas.schemas import TareaCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.logica_procesamiento import apply_transformations
from app.crud.tareas import create_tarea, create_tareas_bulk
from app.core.auth import get_current_active_user
from app.models.models import User
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends

upload_router = APIRouter()

@upload_router.post("/upload", summary="Sube, Transforma y Guarda")
async def Upload_tareas_file(
    file: UploadFile = File(..., description="Archivo CSV o Excel con Datos"),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Sube un archivo, aplica transformaciones y Guarda los resultados en la base de datos de forma asíncrona
    """

    # 1. --- Lectura del Archivo ---
    content_type = file.content_type
    content = await file.read()

    try:
        if content_type == 'text/csv':
            df_initial = pd.read_csv(BytesIO(content), dtype=str)
        elif content_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:    
            df_initial = pd.read_excel(BytesIO(content), engine='openpyxl', dtype=str)
        else:
            raise ValueError("Tipo de archivo no soportado")     
    except Exception as e:    
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al leer el archivo: {e}")


         # 2. --- Normalizar Cabeceras ---
    # Convertir todas las cabeceras a minúsculas y quitar acentos
    def normalize_column_name(text):
        # Convertir a minúsculas primero
        text = text.lower()
        # Quitar acentos
        replacements = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n'}
        for accent, replacement in replacements.items():
            text = text.replace(accent, replacement)
        # Reemplazar espacios y caracteres especiales por guiones bajos
        text = text.replace(' ', '_')
        text = text.replace('(', '_').replace(')', '_')
        text = text.replace('-', '_')
        # Limpiar múltiples guiones bajos consecutivos
        while '__' in text:
            text = text.replace('__', '_')
        # Quitar guiones bajos al inicio y final
        text = text.strip('_')
        return text
    
    # Debug: mostrar columnas originales
    print(f"Columnas originales: {list(df_initial.columns)}")
    
    # Aplicar normalización paso a paso para debug
    new_column_names = []
    for col in df_initial.columns:
        normalized = normalize_column_name(col)
        new_column_names.append(normalized)
        print(f"'{col}' -> '{normalized}'")
    
    # Forzar la aplicación de los nuevos nombres
    df_initial.columns = new_column_names
    
    # Debug: mostrar columnas después de normalización
    print(f"Columnas normalizadas: {list(df_initial.columns)}")
    
    # 3. --- Preparar para Inserción ---
    try:
        # Convertir strings vacíos a None para campos datetime
        date_fields = ['fecha_de_creacion', 'fechas_solicitud_almacen', 'fecha_liberacion_almacen', 
                      'fecha_entrega_en_sitio', 'fecha_solicitud_a_proveedor', 'fecha_de_envio_del_proveedor', 
                      'fecha_entrega_en_sitio_spms']
        
        for field in date_fields:
            if field in df_initial.columns:
                df_initial[field] = df_initial[field].replace('', None)
        
        
        # Aplicar transformaciones que incluyen cálculos
        df_transformed = apply_transformations(df_initial) 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en la transformación: {e}")   
    
    #3. --- Inserción de datos ----

    # Limpiar campos de fecha PRIMERO - convertir NaT a None
    date_fields = ['fecha_de_creacion', 'fechas_solicitud_almacen', 'fecha_liberacion_almacen', 
                  'fecha_entrega_en_sitio', 'fecha_solicitud_a_proveedor', 'fecha_de_envio_del_proveedor', 
                  'fecha_entrega_en_sitio_spms']
    
    for field in date_fields:
        if field in df_transformed.columns:
            # Convertir cualquier valor problemático a None
            df_transformed[field] = df_transformed[field].astype(str)
            df_transformed[field] = df_transformed[field].replace(['NaT', 'nan', 'None', ''], None)
            df_transformed[field] = df_transformed[field].where(df_transformed[field].notna(), None)
    
    # Limpiar campos numéricos - convertir NaN a None
    numeric_fields = ['tiempo_1', 'horas_1', 'tiempo_2', 'horas_2', 'tiempo_3', 'horas_3']
    for field in numeric_fields:
        if field in df_transformed.columns:
            df_transformed[field] = df_transformed[field].where(pd.notna(df_transformed[field]), None)
    
    # Limpiar el resto de campos string - convertir NaN a strings vacíos
    string_fields = [col for col in df_transformed.columns if col not in date_fields + numeric_fields]
    for field in string_fields:
        df_transformed[field] = df_transformed[field].fillna('')

    data_to_insert = df_transformed.to_dict('records')

    # Validar todos los registros primero
    valid_data = []
    errors = []
    
    for index, tarea_data in enumerate(data_to_insert):
        try:
            tarea_in = TareaCreate(**tarea_data)
            valid_data.append(tarea_in.dict())
        except Exception as e:
            tarea_id = tarea_data.get('id_tarea', 'N/A')
            errors.append(f"Fila {index + 2} (Tarea: {tarea_id}): Error de validación - {e}")
    
    # Inserción en lote de registros válidos
    imported_count = 0
    if valid_data:
        try:
            imported_count = await create_tareas_bulk(db=db, tareas_data=valid_data)
        except Exception as e:
            errors.append(f"Error en inserción masiva: {e}")    

    if errors:
        return{
            "message": f"Se importaron {imported_count} tareas, pero {len(errors)} tuvieron errores de DB/validación.",
            "status_code": status.HTTP_207_MULTI_STATUS,
            "errors": errors
        }        

    return {
        "message": f"Archivo Procesado y Transformado con éxito. Se importaron {imported_count} tareas."
    }    