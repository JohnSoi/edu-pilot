from fastapi import APIRouter

from app.core.config import Settings, get_settings
from app.core.database import check_db_connection
from app.schemas.base import AppStatusResponse

base_router: APIRouter = APIRouter()

setting: Settings = get_settings()


@base_router.get("/health", tags=["base"], description="Проверка состояния приложения")
async def get_health() -> bool:
    return True


if setting.DEBUG:
    @base_router.get("/status", tags=["base"], description="Статус работы приложения")
    async def get_app_status() -> AppStatusResponse:
        db_data: dict = await check_db_connection()

        return AppStatusResponse(
            app_start=True, db_connecting=db_data["status"] == "healthy", db_data=db_data, env=setting.ENVIRONMENT
        )

    @base_router.get("/app_init", tags=["base"], description="Инициализация базовых данных приложения")
    async def init_app() -> dict:
        return {}
