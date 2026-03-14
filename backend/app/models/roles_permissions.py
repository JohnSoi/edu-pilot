from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.consts.access import AccessLevel
from .base import BaseModel


class RolesPermissions(BaseModel):
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    permission_id: Mapped[int] = mapped_column(ForeignKey('permissions.id'))
    level_access: Mapped[AccessLevel] = mapped_column(
        PG_ENUM(AccessLevel, name="access_level"),
        nullable=False,
        default=AccessLevel.FORBIDDEN
    )