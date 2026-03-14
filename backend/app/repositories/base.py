from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import Select, select
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

    async def list(self, sorting: dict | None = None, filters: dict | None = None, navigation: dict | None = None) -> list[T]:
        query: Select = select(self._MODEL)

        sorting, filters, navigation = await self._before_list(sorting, filters, navigation)

        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(self._MODEL, key) == value)

        if sorting:
            for key, value in sorting.items():
                query = query.order_by(getattr(self._MODEL, key).desc() if value == "desc" else getattr(self._MODEL, key).asc())

        if navigation:
            query = query.offset((navigation.get("page") - 1) * navigation.get("limit")).limit(navigation.get("limit"))

        result = await self._db.execute(query)

        return list(result.scalars().all()) or []

    async def get(self, entity_id: int) -> T | None:
        return await self._db.get(self._MODEL, entity_id)

    async def get_by_uuid(self, uuid: UUID) -> T | None:
        if not hasattr(self._MODEL, "uuid"):
            return None

        query: Select = select(self._MODEL).filter_by(uuid=uuid)
        result = await self._db.execute(query)

        return result.scalar_one_or_none()

    async def get_by(self, **kwargs) -> T | None:
        query: Select = select(self._MODEL).filter_by(**kwargs)
        result = await self._db.execute(query)

        return result.scalar_one_or_none()

    async def _before_create(self, payload: dict) -> None: ...

    async def _after_create(self, new_entity: T, payload: dict) -> None: ...

    async def _before_list(self, sorting: dict | None = None, filters: dict | None = None, navigation: dict | None = None) -> tuple[dict, ...]:
        return sorting or {}, filters or {}, navigation or {}

