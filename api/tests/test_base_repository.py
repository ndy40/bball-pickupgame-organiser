import pytest

from db.model import User


@pytest.mark.asyncio
async def test_we_can_add_to_db(base_repository):
    user = User(username="user1")
    result = await base_repository.save(user)
    assert isinstance(result, User)
    assert result.id == 1


@pytest.mark.asyncio
async def test_repo_get_model(base_repository):
    model = await base_repository.get(User, 1)
    assert isinstance(model, User)


@pytest.mark.asyncio
async def test_repo_gets_none_for_missing_model(base_repository):
    model = await base_repository.get(User, 100)
    assert model is None


@pytest.mark.asyncio
async def test_repo_delete(base_repository):
    user = User(username="user2")
    new_user = await base_repository.save(user)
    tmp_id = new_user.id
    await base_repository.delete(new_user)
    find_user = await base_repository.get(User, tmp_id)
    assert find_user is None
