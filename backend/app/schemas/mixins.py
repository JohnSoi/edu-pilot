from datetime import datetime
from uuid import UUID


class UuidMixin:
    uuid: UUID


class TimestampMixin:
    created_at: datetime
    updated_at: datetime


class SoftDeleteMixin:
    deleted_at: datetime | None
