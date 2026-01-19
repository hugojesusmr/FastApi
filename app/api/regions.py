from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, delete
from sqlalchemy import String
import pandas as pd
from app.db.session import get_session
from app.schemas.schemas import RegionCreate, RegionRead
from app.models.models import Region

router = APIRouter(tags=["regions"])

@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    try:
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Solo se aceptan archivos Excel")
        
        contents = await file.read()
        df = pd.read_excel(contents)
        
        column_mapping = {
            'Id': 'id',
            'Site_code': 'site_code',
            'location_name': 'location_name',
            'Service PANDA': 'service_panda',
            'city': 'city',
            'state': 'state',
            'TIPO DE RED': 'tipo_de_red',
            'REGION': 'region',
            'COORDIANDOR': 'coordinador',
            'INGENIERO': 'ingeniero',
            'KM': 'km',
            'Ingenieria': 'ingenieria',
            'kmz': 'kmz'
        }
        
        df = df.rename(columns=column_mapping)
        df = df.where(pd.notna(df), None)
        
        regions = [Region(**row.to_dict()) for _, row in df.iterrows()]
        
        await session.exec(delete(Region))
        session.add_all(regions)
        await session.commit()
        
        return {
            "message": f"Se cargaron {len(regions)} registros exitosamente",
            "count": len(regions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[RegionRead])
async def list_regions(
    skip: int = 0,
    limit: int = 10000,
    search: str = None,
    id: int = None,
    site_code: str = None,
    location_name: str = None,
    service_panda: str = None,
    city: str = None,
    state: str = None,
    tipo_de_red: str = None,
    region: str = None,
    coordinador: str = None,
    ingeniero: str = None,
    km: str = None,
    ingenieria: str = None,
    kmz: str = None,
    session: AsyncSession = Depends(get_session)
):
    query = select(Region)
    
    if search and search.strip():
        search_term = f"%{search.strip()}%"
        query = query.where(
            (Region.id.cast(String).ilike(search_term)) |
            (Region.site_code.ilike(search_term)) |
            (Region.location_name.ilike(search_term)) |
            (Region.service_panda.ilike(search_term)) |
            (Region.city.ilike(search_term)) |
            (Region.state.ilike(search_term)) |
            (Region.tipo_de_red.ilike(search_term)) |
            (Region.region.ilike(search_term)) |
            (Region.coordinador.ilike(search_term)) |
            (Region.ingeniero.ilike(search_term)) |
            (Region.km.cast(String).ilike(search_term)) |
            (Region.ingenieria.ilike(search_term)) |
            (Region.kmz.ilike(search_term))
        )
    
    if id:
        query = query.where(Region.id == id)
    if site_code and site_code.strip():
        query = query.where(Region.site_code.ilike(f"%{site_code.strip()}%"))
    if location_name and location_name.strip():
        query = query.where(Region.location_name.ilike(f"%{location_name.strip()}%"))
    if service_panda and service_panda.strip():
        query = query.where(Region.service_panda.ilike(f"%{service_panda.strip()}%"))
    if city and city.strip():
        query = query.where(Region.city.ilike(f"%{city.strip()}%"))
    if state and state.strip():
        query = query.where(Region.state.ilike(f"%{state.strip()}%"))
    if tipo_de_red and tipo_de_red.strip():
        query = query.where(Region.tipo_de_red.ilike(f"%{tipo_de_red.strip()}%"))
    if region and region.strip():
        query = query.where(Region.region.ilike(f"%{region.strip()}%"))
    if coordinador and coordinador.strip():
        query = query.where(Region.coordinador.ilike(f"%{coordinador.strip()}%"))
    if ingeniero and ingeniero.strip():
        query = query.where(Region.ingeniero.ilike(f"%{ingeniero.strip()}%"))
    if km and km.strip():
        query = query.where(Region.km.cast(String).ilike(f"%{km.strip()}%"))
    if ingenieria and ingenieria.strip():
        query = query.where(Region.ingenieria.ilike(f"%{ingenieria.strip()}%"))
    if kmz and kmz.strip():
        query = query.where(Region.kmz.ilike(f"%{kmz.strip()}%"))
    
    query = query.offset(skip).limit(limit)
    result = await session.exec(query)
    return result.all()

@router.get("/{region_id}", response_model=RegionRead)
async def get_region(region_id: int, session: AsyncSession = Depends(get_session)):
    region = await session.get(Region, region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Región no encontrada")
    return region


