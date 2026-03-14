from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.consts.access import AccessLevel
from .base import BaseModel


class RolesPermissions(BaseModel):
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey('permissions.id'), primary_key=True)
    level_access: Mapped[AccessLevel] = mapped_column(
        PG_ENUM(AccessLevel, name="access_level", create_type=False),
        nullable=False, 
        default=AccessLevel.FORBIDDEN
    )