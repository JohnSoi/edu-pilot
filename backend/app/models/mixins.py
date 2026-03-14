from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQL_UUID
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class UuidMixin:
    uuid: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), default=uuid4)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    @property
    def is_new(self):
        return self.created_at == self.updated_at


class SoftDeleteMixin:
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now()
