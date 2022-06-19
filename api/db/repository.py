from typing import AsyncIterable, Dict, Protocol
from sqlalchemy import select

from .model import Base, User, Session


class AbstractRepository(Protocol):
    async def save(self, o: Base) -> Base:
        """save a new entity"""

    async def get(self, model_id: int) -> Base:
        """fetch an entity by id"""

    async def delete(self, model_id: int) -> None:
        """delete an entity"""

    async def list(self, filters: Dict = None) -> AsyncIterable[Base]:
        """return an async iterable"""


class BaseRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    async def save(self, o: Base) -> Base:
        async with self.session() as session:
            async with session.begin():
                session.add(o)
            await session.refresh(o)
        return o

    async def add(self, o: Base) -> Base:
        return await self.save(o)

    async def get(self, model: Base, model_id: int) -> Base:
        async with self.session() as session:
            return await session.get(model, model_id)

    async def get_one(self, model: Base, filters: Dict) -> Base:
        stmt = select(model)

        for field, value in filters.items():
            if hasattr(model, field):
                # add support for multi-filtering by types at some points. E.g like for strings search
                stmt = stmt.where(getattr(model, field) == value)

        async with self.session() as session:
            result = await session.execute(stmt)
            return result.one_or_none()

    async def delete(self, model: Base) -> None:
        async with self.session() as session:
            async with session.begin():
                await session.delete(model)

    async def list(self, model: Base, filters: Dict = None) -> AsyncIterable[Base]:
        return await super().list(filters)


class UserRepository(BaseRepository):
    async def get(self, model_id: int) -> Base:
        return await super().get(User, model_id)


class SessionRespository(BaseRepository):
    async def get(self, model_id: int) -> Base:
        return await super().get(Session, model_id)
