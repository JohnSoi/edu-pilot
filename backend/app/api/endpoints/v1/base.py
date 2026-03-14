from datetime import datetime

from fastapi import APIRouter

from app.core.config import Settings, get_settings
from app.core.database import check_db_connection
from app.core.database.utils import get_db_context
from app.core.security import ADMIN_ROLE_CODE
from app.schemas.base import AppStatusResponse
from app.schemas.users import UserRegisterData
from app.services.roles import RoleService
from app.services.users import UserService

base_router: APIRouter = APIRouter()

setting: Settings = get_settings()


@base_router.get("/health", tags=["base"], description="Проверка состояния приложения")
async def get_health() -> bool:
    return True


if setting.DEBUG:
    @base_router.get("/status", tags=["base"], description="Статус работы приложения")
    async def get_app_status() -> AppStatusResponse:
        db_data: dict = await check_db_connection()

        db_connecting: bool = db_data["status"] == "healthy"
        has_user_admin: bool = False
        has_all_roles: bool = False

        if db_connecting:
            async with get_db_context() as db:
                has_user_admin = await UserService(db).has_admin_user()
                has_all_roles = bool(not await RoleService(db).get_need_roles())

        return AppStatusResponse(
            app_start=True, db_connecting=db_connecting, db_data=db_data, env=setting.ENVIRONMENT,
            has_user_admin=has_user_admin, has_all_roles=has_all_roles
        )

    @base_router.get("/app_init", tags=["base"], description="Инициализация базовых данных приложения")
    async def init_app() -> bool:
        db_data: dict = await check_db_connection()
        db_connecting: bool = db_data["status"] == "healthy"

        if not db_connecting:
            return False

        async with get_db_context() as db:
            if need_add_roles := await RoleService(db).get_need_roles():
                await RoleService(db).create_base_roles(need_add_roles)

            if not await UserService(db).has_admin_user():
                await UserService(db).create_admin_user()

        return True
