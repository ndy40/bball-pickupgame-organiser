import pytest

from db.model import User


@pytest.mark.asyncio
async def test_find_username(user_repository):
    user = await user_repository.find_username(username='user1')
    assert isinstance(user, User)
