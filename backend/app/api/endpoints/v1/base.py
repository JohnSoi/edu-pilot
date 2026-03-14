from fastapi import APIRouter

from app.core.config import get_settings, Settings
from app.core.database import check_db_connection
from app.schemas.base import AppStatusResponse

base_router: APIRouter = APIRouter()

setting: Settings = get_settings()


@base_router.get("/health", tags=["base"])
async def get_health() -> bool:
    return True


if setting.DEBUG:
    @base_router.get("/status", tags=["base"])
    async def get_app_status() -> AppStatusResponse:
        db_data: dict = await check_db_connection()

        return AppStatusResponse(
            app_start=True,
            db_connecting=db_data["status"] == "healthy",
            db_data=db_data,
            env=setting.ENVIRONMENT
        )
