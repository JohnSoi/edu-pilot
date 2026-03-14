from app.models import Roles

from .base import BaseRepository
from ..core.security import ADMIN_ROLE_CODE, DIRECTOR_ROLE_CODE


class RoleRepository(BaseRepository[Roles]):
    _MODEL: type[Roles] = Roles

    async def get_id_by_code(self, role_code: str) -> int | None:
        if not role_code:
            return None

        result: Roles = await self.get_by(code=role_code)

        return result.id if result else None
