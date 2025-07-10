from io import BytesIO
import pandas as pd
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.crud.incidence import create_incidence
from app.schemas.incidence import IncidenceCreate
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

upload_router = APIRouter()

@upload_router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
        Sube un archivo Excel y guarda sus registros en la Base de Datos.
    """
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Archivo no Valido")

    contents = await file.read()

    try:
        excel_file = BytesIO(contents)
        df = pd.read_excel(excel_file, engine="openpyxl")
        df = df.fillna("")
        
       # df["inicio_de_falla"]= df["inicio_de_falla"].fillna('')
        records = df.to_dict("records")

        for record in records:
            incidence_data = IncidenceCreate(
                number = record["number"],
                inicio_de_falla=record["inicio_de_falla"],
                fecha_de_envio=record["fecha_de_envio"],
                fecha_resolucion_falla=record["fecha_resolucion_falla"],
                priority=record["priority"],
                actual_assignment_group=record["actual_assignment_group"],
                state=record["state"],
                resolution_code_n1=record["resolution_code_n1"],
                resolution_code_n2=record["resolution_code_n2"],
                resolution_code_n3=record["resolution_code_n3"],
                resolution_notes=record["resolution_notes"],
                afectacion_al_servicio=record["afectacion_al_servicio"],
                category_ci=record["category_ci"],
                cmdb_ci=record["cmdb_ci"])
            create_incidence(db, incidence_data)
        return {"message":f"Archivo {file.filename} procesado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Procesando Archivo: {e}")    