import pytest

from db.model import User
from services.user_service import authenticate, register


@pytest.mark.asyncio
async def test_find_username(user_repository):
    user = await user_repository.find_username(username="user1")
    assert isinstance(user, User)


@pytest.mark.asyncio
async def test_user_authentication_fails_with_no_user(user_repository):
    non_user = await authenticate("user#100")
    assert non_user is None


@pytest.mark.asyncio
async def test_user_authentication(user_repository):
    token = await authenticate("user#1")
    assert isinstance(token, str)


@pytest.mark.asyncio
@pytest.mark.parametrize('input,exp', [('a', None), ('ab', None), ('abc', None)])
async def test_user_registration_fails(input, exp):
    assert await register(input) == exp


@pytest.mark.asyncio
async def test_user_registration_succeeds():
    user = await register('new_user_hope')
    assert isinstance(user, User)
