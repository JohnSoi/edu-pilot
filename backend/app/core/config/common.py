import warnings
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .consts import BASE_POSTGRES_PASSWORD, BASE_SECRET_KEY
from .types import CorsValueType
from .utils import get_or_create_app_version, get_valid_cors, get_valid_db_url, get_valid_redis_url
from .validators import get_valid_app_version


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Основные настройки
    APP_NAME: str = "FastAPI Example"
    APP_VERSION: str | None = None
    APP_DESCRIPTION: str = "FastAPI Example Description"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: Literal["development", "test", "production"] = "production"

    # Безопасность
    SECRET_KEY: str = BASE_SECRET_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 дней
    PASSWORD_MIN_LENGTH: int = 8

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Настройки базы данных
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = BASE_POSTGRES_PASSWORD
    POSTGRES_DB: str = "example_db"
    POSTGRES_SCHEMA: str = "public"
    POSTGRES_ENGINE: str = "asyncpg+postgresql"

    # Настройки соединения с БД
    DATABASE_URL: str | None = None
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_ECHO: bool = False

    # Настройки Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int = 0
    REDIS_SSL: bool = False
    REDIS_URL: str | None = None

    # Настройки кеширования
    CACHE_TTL: int = 5 * 60  # 5 минут
    CACHE_PREFIX: str = "cache_prefix_example:"

    # Настройки логирования
    LOG_LEVEL: Literal["INFO", "DEBUG", "WARNING", "ERROR"] = "WARNING"
    LOG_FORMAT: str = "json"
    LOG_FILE: str | None = None

    # Настройки email
    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_USE_TLS: bool = True
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    # Лимитирование запросов
    RATE_LIMIT_ENABLE: bool = True
    RATE_LIMIT_REQUEST: int = 100  # запросов
    RATE_LIMIT_PERIOD: int = 60  # в минуту

    @property
    def is_dev_env(self) -> bool:
        return self.ENVIRONMENT != "production"

    @field_validator("APP_VERSION", mode="before")
    @classmethod
    def set_app_version(cls, v: str | None) -> str:
        return get_or_create_app_version(v)

    @field_validator("APP_VERSION")
    @classmethod
    def validate_app_version(cls, v: str) -> str:
        return get_valid_app_version(v)

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: CorsValueType) -> CorsValueType:
        return get_valid_cors(v)

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info) -> str:
        return get_valid_db_url(v, info.data)

    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_connection(cls, v: str | None, info) -> str:
        return get_valid_redis_url(v, info.data)


def get_settings() -> Settings:
    settings: Settings = Settings()

    if settings.is_dev_env:
        return settings

    if settings.SECRET_KEY == BASE_SECRET_KEY:
        warnings.warn('Поле "SECRET_KEY" имеет значение по умолчанию. Его необходимо сменить', RuntimeWarning)

    if settings.POSTGRES_PASSWORD == BASE_POSTGRES_PASSWORD:
        warnings.warn('Поле "POSTGRES_PASSWORD" имеет значение по умолчанию. Его необходимо сменить', RuntimeWarning)

    if not settings.REDIS_PASSWORD:
        warnings.warn('Поле "REDIS_PASSWORD" не задано. необходимо использовать пароль', RuntimeWarning)

    if not settings.DB_ECHO and settings.is_dev_env:
        warnings.warn("Отключен вывод запросов в dev среде", RuntimeWarning)

    return settings
