from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import UuidMixin, TimestampMixin, SoftDeleteMixin


class Users(BaseModel, UuidMixin, TimestampMixin, SoftDeleteMixin):
    surname: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    patronymic: Mapped[str] = mapped_column(String(50), nullable=True)

    login: Mapped[str] = mapped_column(String(50), index=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(150), nullable=False)

    date_deactivate: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    date_birthday: Mapped[date] = mapped_column(Date, nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), primary_key=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'), primary_key=True)

    role = relationship("Roles")
    branch = relationship("Branches")

