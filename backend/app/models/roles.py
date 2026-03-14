from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import UuidMixin


class Roles(BaseModel, UuidMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    # Связь с разрешениями через ассоциативную таблицу
    permissions = relationship("Permissions", secondary="roles_permissions")
