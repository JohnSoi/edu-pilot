from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import require_roles
from app.api.dependencies.database import get_db
from app.core.security import ADMIN_ROLE_CODE, DIRECTOR_ROLE_CODE
from app.schemas.security import TokenData
from app.schemas.users import UserPublicData, UserRegisterData
from app.services.users import UserService

users_api: APIRouter = APIRouter(prefix="/users", tags=["users"])


@users_api.put("/", response_model=UserPublicData, description="Создание нового пользователя")
async def create_user(
    user_data: UserRegisterData,
    db: AsyncSession = Depends(get_db),
    current_user: TokenData = Depends(require_roles([ADMIN_ROLE_CODE, DIRECTOR_ROLE_CODE])),
) -> dict:
    return await UserService(db).create(user_data, current_user)
