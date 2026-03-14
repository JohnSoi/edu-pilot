from app.models import Users

from .base import BaseRepository


class UserRepository(BaseRepository[Users]):
    _MODEL: type[Users] = Users
