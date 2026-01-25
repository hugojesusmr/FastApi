from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession 

engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionFactory = sessionmaker(engine , class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise    
        finally:  
            await session.close()

