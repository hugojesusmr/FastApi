from sqlmodel import Session, select
from app.models.models import Region
from app.schemas.schemas import RegionCreate, RegionUpdate

def create_region(session: Session, region: RegionCreate) -> Region:
    db_region = Region.from_orm(region)
    session.add(db_region)
    session.commit()
    session.refresh(db_region)
    return db_region

def create_regions_bulk(session: Session, regions: list[RegionCreate]) -> list[Region]:
    db_regions = [Region.from_orm(region) for region in regions]
    session.add_all(db_regions)
    session.commit()
    return db_regions

def get_region(session: Session, region_id: int) -> Region:
    return session.get(Region, region_id)

def get_regions(session: Session, skip: int = 0, limit: int = 100) -> list[Region]:
    statement = select(Region).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_region_by_site_code(session: Session, site_code: str) -> Region:
    statement = select(Region).where(Region.site_code == site_code)
    return session.exec(statement).first()

def update_region(session: Session, region_id: int, region_update: RegionUpdate) -> Region:
    db_region = session.get(Region, region_id)
    if db_region:
        region_data = region_update.dict(exclude_unset=True)
        for key, value in region_data.items():
            setattr(db_region, key, value)
        session.add(db_region)
        session.commit()
        session.refresh(db_region)
    return db_region

def delete_region(session: Session, region_id: int) -> bool:
    db_region = session.get(Region, region_id)
    if db_region:
        session.delete(db_region)
        session.commit()
        return True
    return False

def delete_all_regions(session: Session) -> int:
    statement = select(Region)
    regions = session.exec(statement).all()
    for region in regions:
        session.delete(region)
    session.commit()
    return len(regions)
