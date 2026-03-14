from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import SoftDeleteMixin, TimestampMixin, UuidMixin


class Branches(BaseModel, UuidMixin, TimestampMixin, SoftDeleteMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    geo: Mapped[dict] = mapped_column(JSON, nullable=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=False)

    region = relationship("Regions")
