from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class Permissions(BaseModel):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
