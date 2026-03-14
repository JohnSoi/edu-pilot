from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel

T: TypeVar = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    _MODEL: T

    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def create(self, payload: dict) -> T:
        new_entity: T = self._MODEL()

        await self._before_create(payload)

        for key, value in payload.items():
            if hasattr(new_entity, key):
                setattr(new_entity, key, value)

        self._db.add(new_entity)
        await self._db.commit()
        await self._db.flush(new_entity)

        await self._after_create(new_entity, payload)

        return new_entity

    async def _before_create(self, payload: dict) -> None: ...

    async def _after_create(self, new_entity: T, payload: dict) -> None: ...
