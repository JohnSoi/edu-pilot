import contextlib
from typing import Any, AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from .common import AsyncSessionLocal, async_engine


@contextlib.asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            session.close()


async def get_db_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.connect() as connection:
        yield connection


async def check_db_connection() -> dict[str, Any]:
    """
    Проверка подключения к БД (для health checks)
    """
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            await conn.commit()

        # Получаем информацию о БД
        async with async_engine.connect() as conn:
            result = await conn.execute(text("""
                    SELECT 
                        current_database() as db_name,
                        current_user as db_user,
                        version() as version
                """))
            db_info = result.first()

        return {
            "status": "healthy",
            "database": db_info[0] if db_info else "unknown",
            "user": db_info[1] if db_info else "unknown",
            "version": db_info[2][:50] + "..." if db_info else "unknown",
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
