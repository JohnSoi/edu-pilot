from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, declarative_base, declared_attr, mapped_column

from app.utils.text import camel_to_snake


class CustomBaseModel:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)


BaseModel = declarative_base(cls=CustomBaseModel)
