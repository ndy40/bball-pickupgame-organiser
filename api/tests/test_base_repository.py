import pytest

from db.repository import BaseRepository
from db.connect import async_session
from db.model import User


@pytest.mark.asyncio
async def test_we_can_add_to_db():
    repo = BaseRepository(async_session)
    user = User(username='user1')
    result = await repo.save(user)
    assert isinstance(result, User)
    assert result.id == 1
