from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.consts.contacts import ContactType

from .base import BaseModel
from .mixins import TimestampMixin, UuidMixin


class Contacts(BaseModel, UuidMixin, TimestampMixin):
    value: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[ContactType] = mapped_column(PG_ENUM(ContactType, name="contact_type"), nullable=False)
    validated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"), nullable=True)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
