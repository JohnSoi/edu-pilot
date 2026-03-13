from datetime import date, datetime
from typing import Any

from .consts import VERSION_PART_LENGTH, CORS_LIST_SYMBOL_START, CORS_LIST_DELIMITER
from .exceptions import InvalidCorsValue, EmptyDbSettings
from .types import CorsValueType, PydanticSettingsInfoType


def get_or_create_app_version(version: str | None) -> str:
    if version:
        return version

    current_date: date = datetime.now().date()

    return f"{str(current_date.year)[:VERSION_PART_LENGTH]}.{str(current_date.month).zfill(VERSION_PART_LENGTH)}"


def get_valid_cors(value: CorsValueType) -> CorsValueType:
    if isinstance(value, str) and not value.startswith(CORS_LIST_SYMBOL_START):
        return [i.strip() for i in value.split(CORS_LIST_DELIMITER)]

    if isinstance(value, list | str):
        return value

    raise InvalidCorsValue(value)


def get_valid_db_url(value: Any | None, settings_data: PydanticSettingsInfoType) -> str:
    if value and isinstance(value, str):
        return value

    if not all(
        map(
            bool,
            (
                settings_data.get(field)
                for field in (
                    "POSTGRES_ENGINE",
                    "POSTGRES_USER",
                    "POSTGRES_PASSWORD",
                    "POSTGRES_HOST",
                    "POSTGRES_PORT",
                    "POSTGRES_DB",
                )
            ),
        )
    ):
        raise EmptyDbSettings()

    return (
        f"{settings_data.get('POSTGRES_ENGINE')}://{settings_data.get('POSTGRES_USER')}"
        f":{settings_data.get('POSTGRES_PASSWORD')}@{settings_data.get('POSTGRES_HOST')}"
        f":{settings_data.get('POSTGRES_PORT')}/{settings_data.get('POSTGRES_DB')}"
    )


def get_valid_redis_url(value: Any | None, settings_data: PydanticSettingsInfoType) -> str:
    if value and isinstance(value, str):
        return value

    auth_part: str = f":{settings_data.get("REDIS_PASSWORD")}@" if settings_data.get("REDIS_PASSWORD") else ""
    ssl_part: str = "?ssl=true" if settings_data.get("REDIS_SSL", False) else ""

    return (
        f"redis://{auth_part}{settings_data.get("REDIS_HOST")}:"
        f"{settings_data.get("REDIS_PORT")}/{settings_data.get("REDIS_DB")}{ssl_part}"
    )
