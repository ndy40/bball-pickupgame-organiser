import os

from alembic.config import Config
from alembic.command import upgrade


def pytest_sessionstart():
    alembic_config = Config("alembic.ini")
    alembic_config.set_section_option("alembic", "sqlalchemy.url", os.environ["DB_FILE"])
    upgrade(alembic_config, "head")


def pytest_sessionfinish():
    if os.path.isfile("bball_test.db"):
        os.remove("bball_test.db")
