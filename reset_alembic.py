import asyncio
from sqlalchemy import text
from app.db.session import engine

async def reset_alembic():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
            print("✅ Tabla alembic_version eliminada")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(reset_alembic())
