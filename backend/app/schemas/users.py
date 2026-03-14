from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.core.config import get_settings, Settings
from app.core.security import validate_password_strength
from .mixins import UuidMixin
from ..exceptions.base import ValidationError

settings: Settings = get_settings()


class UserPersonData(BaseModel):
    surname: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=2, max_length=50)
    patronymic: str | None = Field(None, max_length=50)
    date_birthday: date

    @field_validator("date_birthday")
    @classmethod
    def validate_date_birthday(cls, v: date) -> date:
        today: date = date.today()

        if v > today:
            raise ValidationError("Дата рождения не может быть в будущем")

        four_years_ago: date = today.replace(year=today.year - settings.MIN_USER_AGE)

        if v > four_years_ago:
            raise ValidationError(f"Минимальный возраст — {settings.MIN_USER_AGE} года")
        return v


class UserAuthData(BaseModel):
    login: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=settings.PASSWORD_MIN_LENGTH, max_length=20)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        valid, error = validate_password_strength(v)

        if valid:
            return v

        raise ValidationError(error)


class UserRegisterData(UserPersonData, UserAuthData):
    role_code: str
    branch_uuid: UUID | None = None


class UserPublicData(UuidMixin, UserPersonData): ...
