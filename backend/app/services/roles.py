from .base import BaseService
from app.models import Roles
from app.repositories.roles import RoleRepository
from app.schemas.roles import RoleCreateData
from ..core.security import ADMIN_ROLE_CODE, DIRECTOR_ROLE_CODE
from ..core.security.consts import STUDENT_ROLE_CODE, TEACHER_ROLE_CODE, MANAGER_ROLE_CODE, MANAGER_LEARNING_ROLE_CODE


class RoleService(BaseService[RoleRepository, RoleCreateData, Roles]):
    _REPOSITORY: RoleRepository = RoleRepository
    _BASE_ROLES: tuple[tuple[str, str], ...] = (
        ("Администратор", ADMIN_ROLE_CODE),
        ("Руководитель", DIRECTOR_ROLE_CODE),
        ("Менеджер по продажам", MANAGER_ROLE_CODE),
        ("Менеджер учебного процесса", MANAGER_LEARNING_ROLE_CODE),
        ("Преподаватель", TEACHER_ROLE_CODE),
        ("Студент", STUDENT_ROLE_CODE),
    )

    async def create_base_roles(self, need_roles_create: list[str] | None = None) -> None:
        roles: tuple[tuple[str, str], ...] = self._BASE_ROLES

        if need_roles_create:
            roles = tuple((name, code) for name, code in self._BASE_ROLES if code in need_roles_create)

        for name, code in roles:
            await self._repository.create({"name": name, "code": code})

    async def get_need_roles(self) -> list[str]:
        need_add_roles_codes: list[str] = []

        for _, code in self._BASE_ROLES:
            if not await self._repository.get_id_by_code(code):
                need_add_roles_codes.append(code)

        return need_add_roles_codes

