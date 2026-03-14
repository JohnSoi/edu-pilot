from datetime import datetime

from .base import BaseService
from app.models import Users
from app.repositories.users import UserRepository
from app.schemas.users import UserRegisterData
from .branches import BranchService
from app.core.security import ADMIN_ROLE_CODE
from app.exceptions.users import NoAllowedAddInOtherBranch
from app.schemas.security import TokenData
from ..core.config import Settings, get_settings


class UserService(BaseService[UserRepository, UserRegisterData, Users]):
    _REPOSITORY: UserRepository = UserRepository

    async def register(self, payload: UserRegisterData, current_user: TokenData | None = None) -> Users:
        if not current_user or current_user.role_code == ADMIN_ROLE_CODE:
            return await super().create(payload)

        branch_data = await BranchService(self._db).get_by_uuid(payload.branch_uuid) if payload.branch_uuid else None
        branch_id = branch_data.id if branch_data else None

        if current_user.branch_id != branch_id:
            raise NoAllowedAddInOtherBranch()

        return await super().create(payload)

    async def has_admin_user(self) -> bool:
        return bool(await self.list(
            filters={"role": ADMIN_ROLE_CODE}, navigation={"page": 1, "limit": 1}
        ))

    async def create_admin_user(self) -> Users:
        settings: Settings = get_settings()

        return await self.create(UserRegisterData(
            surname="Администратор", name="Администратор", patronymic="Администратор",
            role_code=ADMIN_ROLE_CODE, password=settings.SECRET_KEY[:15], login="admin",
            date_birthday=datetime.strptime("1970-01-01", "%Y-%m-%d")
        ))
