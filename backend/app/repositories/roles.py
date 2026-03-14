from app.models import Roles

from .base import BaseRepository


class RoleRepository(BaseRepository[Roles]):
    _MODEL: type[Roles] = Roles
