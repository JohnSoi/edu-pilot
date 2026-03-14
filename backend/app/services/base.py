from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel as PyBaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel
from app.repositories.base import BaseRepository

T: TypeVar = TypeVar("T", bound=BaseRepository)
T1: TypeVar = TypeVar("T1", bound=PyBaseModel)
T2: TypeVar = TypeVar("T2", bound=BaseModel)


class BaseService(Generic[T, T1, T2]):
    _REPOSITORY: type[T]

    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db
        self._repository: T = self._REPOSITORY(db)

    async def create(self, payload: T1) -> T2:
        return await self._repository.create(payload.model_dump(exclude_unset=True))

    async def list(self, sorting: dict | None = None, filters: dict | None = None, navigation: dict | None = None) -> list[T2]:
        return await self._repository.list(sorting, filters, navigation)

    async def get(self, entity_id: int) -> T2:
        return await self._repository.get(entity_id)

    async def get_by_uuid(self, uuid: UUID) -> T2:
        return await self._repository.get_by_uuid(uuid)
