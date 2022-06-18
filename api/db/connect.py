from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_async_engine(settings.DB_FILE, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with async_session() as session:
        yield session
