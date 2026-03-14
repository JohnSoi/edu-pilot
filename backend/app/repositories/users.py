from app.models import Users
from app.core.security import get_password_hash

from .base import BaseRepository
from .branches import BranchRepository
from .roles import RoleRepository


class UserRepository(BaseRepository[Users]):
    _MODEL: type[Users] = Users

    async def _before_create(self, payload: dict) -> None:
        if payload.get("password"):
            payload["password"] = get_password_hash(payload["password"])

        payload["role_id"] = await RoleRepository(self._db).get_id_by_code(payload["role_code"])
        del payload["role_code"]

        if payload.get("branch_uuid"):
            payload["branch_id"] = await BranchRepository(self._db).get_by_uuid(payload["branch_uuid"])
            del payload["branch_uuid"]

    async def _before_list(self, sorting: dict | None = None, filters: dict | None = None, navigation: dict | None = None) -> tuple[dict, ...]:
        sorting, filters, navigation = await super()._before_list(sorting, filters, navigation)

        if role_code := filters.get("role"):
            del filters["role"]

            filters["role_id"] = await RoleRepository(self._db).get_id_by_code(role_code)

        return sorting, filters, navigation
