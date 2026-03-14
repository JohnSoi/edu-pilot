from typing import Generic, TypeVar

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

    async def _create(self, payload: T1) -> T2:
        return await self._repository.create(payload.model_dump(exclude_unset=True))
