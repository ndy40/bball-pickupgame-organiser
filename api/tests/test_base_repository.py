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


@pytest.mark.asyncio
async def test_repo_get_one(base_repository):
    await base_repository.add(User(username=f"user#1"))
    result = await base_repository.get_one(User, filters={"username": "user#1"})
    assert isinstance(result[0], User)


@pytest.mark.asyncio
async def test_repo_get_one_returns_none_when_no_result(base_repository):
    result = await base_repository.get_one(User, filters={"username": "user#2"})
    assert result is None


@pytest.mark.asyncio
async def test_repo_list_returns_all_items(base_repository):
    results = await base_repository.list(User)
    assert all(item for item in results if isinstance(item[0], User))


@pytest.mark.asyncio
async def test_repo_list_returns_some_items_with_like(base_repository):
    results = await base_repository.list(User, filters={'username__like': '#1'})
    assert next(results)[0].username == 'user#1'
