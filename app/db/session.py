from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession 

# 1. --- Crear motor de conexión ---
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True,
    future =True)

# 2. --- Generador de sesiónes Factory ----
AsyncSessionFactory = sessionmaker(
    engine , 
    class_=AsyncSession, 
    expire_on_commit=False)

# 3.- Función de Inyección (Dependency)
async def get_session() -> AsyncSession:
    """
    Generador de sesiones para inyección de dependencias
    Principio: Dependency Inversion
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise    
        finally:  
            await session.close()

