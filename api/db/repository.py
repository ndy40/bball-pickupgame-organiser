from typing import AsyncIterable, Dict, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from .model import Base


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

    async def get(self, model_id: int) -> Base:
        return await super().get(model_id)

    async def get_one(self, filters: Dict) -> Base:
        """filter and return the first result"""

    async def delete(self, model_id: int) -> None:
        return await super().delete(model_id)

    async def list(self, filters: Dict = None) -> AsyncIterable[Base]:
        return await super().list(filters)
