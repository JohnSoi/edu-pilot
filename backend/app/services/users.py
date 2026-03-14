from .base import BaseService
from app.models import Users
from app.repositories.users import UserRepository
from app.schemas.users import UserRegisterData


class UserService(BaseService[UserRepository, UserRegisterData, Users]):
    _REPOSITORY: UserRepository = UserRepository
