import os

import pytest
from alembic.config import Config
from alembic.command import upgrade

from db.connect import async_session
from db.repository import BaseRepository, UserRepository


def pytest_sessionstart():
    alembic_config = Config("alembic.ini")
    alembic_config.set_section_option("alembic", "sqlalchemy.url", os.environ["DB_FILE"])
    upgrade(alembic_config, "head")


def pytest_sessionfinish():
    if os.path.isfile("data/bball_test.db"):
        os.remove("data/bball_test.db")


@pytest.fixture
def base_repository():
    return BaseRepository(async_session)


@pytest.fixture
def user_repository():
    return UserRepository(async_session)
