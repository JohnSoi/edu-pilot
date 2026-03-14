from .base import BaseService
from app.models import Roles
from app.repositories.roles import RoleRepository
from app.schemas.roles import RoleCreateData


class RoleService(BaseService[RoleRepository, RoleCreateData, Roles]):
    _REPOSITORY: RoleRepository = RoleRepository
