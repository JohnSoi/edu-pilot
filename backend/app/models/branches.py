from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModel
from .mixins import UuidMixin, TimestampMixin, SoftDeleteMixin


class Branches(BaseModel, UuidMixin, TimestampMixin, SoftDeleteMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    geo: Mapped[dict] = mapped_column(JSON, nullable=True)
    region_id: Mapped[int] = mapped_column(ForeignKey('regions.id'), nullable=False)

    region = relationship("Regions")
